import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="miniDocker",
    version="0.0.1",
    author="Augustus",
    author_email="vermouth7dante@gmail.com",
    description="the middleware and server-side package for WeChat mini program 'miniDocker'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask',
        'requests',
        'wtforms',
        'docker'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
