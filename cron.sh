#!/bin/bash

cd /data/spider/
/data/py3/bin/python /data/spider/main.py >> /data/spider/spider_log 2>&1
echo `date '+%Y-%m-%d_%H:%M:%S'` >> /data/spider/spider_log
sleep 3
echo `ps -ef |grep chrome |grep -v grep |awk '{print $2}' |wc -l` >> /data/spider/spider_log