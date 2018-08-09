### install

```
# install python3
sudo yum install -y epel-release
yum install gcc gcc-devel zlib-devel git  openssl-devel chromium Xvfb  xorg-x11-fonts*
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
echo "source /data/py3/bin/activate" > /data/news_spider/.env

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
# webdirve install(not GUI)
cp /data/spider/core/chromedriver /usr/bin/
vi /usr/bin
tee /usr/bin/xvfb-chromium >EOF
#!/bin/bash

_kill_procs() {
  kill -TERM $chromium
  wait $chromium
  kill -TERM $xvfb
}

# Setup a trap to catch SIGTERM and relay it to child processes
trap _kill_procs SIGTERM

XVFB_WHD=${XVFB_WHD:-1280x720x16}

# Start Xvfb
Xvfb :99 -ac -screen 0 $XVFB_WHD -nolisten tcp &
xvfb=$!

export DISPLAY=:99

chromium --no-sandbox --disable-gpu$@ &
chromium=$!

wait $chromium
wait $xvfb
EOF

ln -s /usr/lib64/chromium-browser/chromium-browser.sh /usr/bin/chromium
mv /usr/bin/chromium-browser ~/
ln -s /usr/bin/xvfb-chromium /usr/bin/chromium-browser
ln -s /usr/bin/xvfb-chromium /usr/bin/google-chrome




```

```
requests 检查状态码
```



```
pip install pipreqs
pipreqs ./ --force
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
# mongod.conf
bind_ip = 10.138.0.33
port = 27017
fork = true
master = true
pidfilepath = /data/mongodb/run/mongodb.pid
logpath = /data/mongodb/log/mongodb.log
dbpath  = /data/mongodb/lib/mongodb
journal = true
directoryperdb = true
logappend = true
#auth = true
#KeyFile=/data/mongodb/keyfile/keyfile
FOE

systemctl enable mongod
systemctl start mongod
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