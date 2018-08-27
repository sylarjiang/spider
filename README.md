### install

```
# install python3
sudo yum install -y epel-release
yum install -y gcc gcc-devel zlib-devel git openssl-devel Xvfb readline-devel xorg-x11-fonts*
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
tar -zxvf Python-3.6.4.tgz
cd Python-3.6.4/
./configure --prefix=/usr/local/python3

make && make install
ln -s /usr/local/python3/bin/python3 /usr/bin/python3

cd /data
python3 -m venv py3



# linux autoenv
git clone git://github.com/kennethreitz/autoenv.git
echo 'source /data/autoenv/activate.sh' >> ~/.bashrc
source ~/.bashrc

# config autoenv
git clone http://192.168.1.234/sylar/news_spider.git
echo "source /data/py3/bin/activate" > /data/spider/.env

pip install -r requirements.txt
```


```
webdrive
https://www.seleniumhq.org/docs/03_webdriver.jsp        #doc
https://sites.google.com/a/chromium.org/chromedriver/downloads #download
http://chromedriver.storage.googleapis.com/2.41/notes.txt #webdrive support chrome version

#https://developers.google.com/web/updates/2017/04/headless-chrome

# http://phantomjs.org/download.html   # version 2.1.1 windows # drop

# https://github.com/mozilla/geckodriver/releases   # firefox drop
```
```
cat << EOF > /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
EOF
yum install google-chrome-stable

cp core/chromedriver /usr/bin/
chmod +x /usr/bin/chromedriver

```

```
# webdirve install(not GUI)
yum install xfvb chrome

and
ln -s /some_path/webdrive /usr/bin/

echo 'Xvfb -ac :99 -screen 0 1280x1024x16 & export DISPLAY=:99' > /etc/rc.d/rc.local

# kill chrome
ps -ef |grep chrome |grep -v grep |awk '{print $2}'|xargs kill -9
```


```
# install mongodb
tee /etc/yum.repos.d/mongodb3.6.repo <<-EOF
[mongodb3.6]
name=MongoDB Repository aliyun
baseurl=https://mirrors.aliyun.com/mongodb/yum/redhat/7Server/mongodb-org/3.6/x86_64/
gpgcheck=0
enabled=1
EOF

yum install mongodb-org-* -y
sudo mkdir /data/mongodb/{run,log,lib/mongodb} -p
sudo chown mongod.mongod -R /data/mongodb

tee /etc/mongod.conf <<-FOE
systemLog:
  destination: file
  logAppend: true
  path: /data/mongodb/log/mongodb.log
storage:
  dbPath: /data/mongodb/lib/mongodb
  journal:
    enabled: true
processManagement:
  fork: true
  pidFilePath: /data/mongodb/run/mongodb.pid
net:
  port: 27017
  bindIp: 0.0.0.0
security:
#  authorization: enabled
  javascriptEnabled: false
FOE

systemctl enable mongod
systemctl start mongod                   
#or : echo "/usr/bin/mongod -f /etc/mongod.conf" >> /etc/rc.d/rc.local
mongo --host 10.138.0.33 --port 27017
### mongo shell

use admin
db.createUser({
    user:"root",
    pwd:"gtl1023",
    roles:[{
        role:"userAdminAnyDatabase",
        db:"admin"
    }]
})


use news_spider
db.createUser({
    user:"news_spider",
    pwd:"gtl1023",
    roles:[{
        role:"dbOwner",
        db:"news_spider"
    }]
})

```


```
cron.sh
#!/bin/bash

cd /data/spider/
/data/py3/bin/python /data/spider/main.py >> /data/spider/spider_log 2>&1
echo `date '+%Y-%m-%d_%H:%M:%S'` >> /data/spider/spider_log
sleep 3
echo `ps -ef |grep chrome |grep -v grep |awk '{print $2}' |wc -l` >> /data/spider/spider_log

echo '--------------------------'

*/60 * * * * /bin/bash /data/spider/cron.sh

```


