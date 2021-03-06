#!/bin/bash

pip install django==1.8
pip install django-mptt
pip install django-tagging
pip install markdown
pip install Pillow

# https 
pip install django-sslify

# 安装PIL
sudo apt-get install python-imaging

## 下面操作没有成功
pip uninstall PIL
# 前提:安装jpeg
sudo apt-get install libjpeg8-dev
pip install PIL
## 没有成功


# celery 启动
# http://docs.celeryproject.org/en/latest/genindex.html
celery worker -A tasks -Q default -l INFO -f logs/celery.server.log -c 4 --time-limit=10 
nohup celery worker -A tasks -l INFO -f logs/celery.server.log -c 2  -P gevent &

# uwsgi
uwsgi --ini scripts/deploy/uwsgi.ini
uwsgi --reload /tmp/uwsgi.deadend.pid

# mysql
mysqldump -u 用户名 -p -t deadend blog_entry > entry.sql

# rm pyc
find . -name "*.pyc" -exec rm {} \;
