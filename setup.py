"""
    to be used like package.json to install deps)))
    dependencies are in install_requires=[]
    dev_dependencies are in extras_require={}
    to plug them in, we do a trick:
    requirements.txt contains "-e .[dev]", so
    pip install -r requirements.txt
    will read this file for dependencies and dev_dependencies
"""
from setuptools import setup

setup(
    name='habroproxy2',
    version='0.2.0',
    description=('An SSL-capable (funny) proxy, test task for applicants to'
                 ' one software company'),
    long_description='',
    author='Yury Danilin',
    author_email='yuvede@gmail.com',
    classifiers=[],
    install_requires=[
        'html5lib==1.0.1',
        'requests==2.19.1',
        'beautifulsoup4==4.6.3',
    ],
    extras_require={
        'dev': [
            'flake8==3.6.0',
            'pytest==3.7.4',
        ]
    }
)
