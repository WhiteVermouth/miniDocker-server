## miniDocker

<img src="miniDocker.png" width="40%" />

微信小程序**miniDocker**的**Middleware**和服务端。

有关微信小程序**miniDocker**可见此[Repo](https://github.com/WhiteVermouth/miniDocker-ui)
    
## 安装前提条件

1. 安装`Python3`

2. 安装`Python3`虚拟环境

	`sudo apt-get install python3-venv`
	
3. 安装`Docker`
	
## 安装

1. `SSH`登录服务器
	
	`ssh yourusername@example.com`

2. 创建`Python3`虚拟环境
	
	```
	cd ~
	python3 -m venv miniDocker
	```

3. 在已创建的虚拟环境中安装`miniDocker` 和 [Gunicorn](http://gunicorn.org/)

	```
	cd miniDocker
	source bin/activate
	pip install miniDocker gunicorn
	deactivate
	```
	
4. 配置`miniDocker`配置文件

	`vim /path/to/miniDocker/config.json`
	
	```
	{
  		"TOKEN": "bb4f564a713a4068a671e13d42bb8bfa",
		"PASSWORD": "miniDocker"
	}
	```
	
	* 配置文件路径可自定义，但需确保当前用户有权限读取
	* 以上范例配置亦为默认配置
	* 若不设置配置文件即采用以上配置（**不推荐**）

5. 安装`supervisor`和`nginx`
	
	```
	sudo apt-get install supervisor
	sudo apt-get install nginx
	```


6. 配置`supervisor`
	
	`sudo vim /etc/supervisor/conf.d/miniDocker-server.conf`
	
	配置内容（对其中内容做相应的修改）:
	
	```
	[program:minidocker-server]
	command=/path/to/pyvenv/gunicorn -w 1 -b 127.0.0.1:4000 app:app
	directory=/path/to/pyvenv/site-packages/miniDocker/server
	environment=MINIDOCKER_CONF="/path/to/miniDocker/config.json"
	user=yourusername
	```
    
7. 配置`Nginx`

	`sudo vim /etc/nginx/conf.d/miniDocker-server.conf`
	
	配置内容（对其中内容做相应的修改）:
	
	```
	server {
		listen 80;
		server_name example.com;
		access_log  /var/log/nginx/miniDocker-server.log;
		error_log  /var/log/nginx/miniDocker-server-error.log;

		location / {
			proxy_pass http://127.0.0.1:4000;
			proxy_set_header Host $host;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		}
	}
	```
	
8. 启动(重加载)`Nginx`和`Supervisor`

	```
	sudo systemctl reload nginx
	sudo supervisorctl reload
	```
    
## 注意事项

* 此安装步骤适用于**Debian 9**，其他系统未做测试
* 此安装步骤中使用的**Docker**为**Docker CE**
* 此安装步骤中使用的**Python**版本为**3.5.3**