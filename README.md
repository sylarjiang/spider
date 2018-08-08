### install

```
python3 -m venv py3
```
```
linux autoenv
git clone git://github.com/kennethreitz/autoenv.git

echo 'source /opt/autoenv/activate.sh' >> ~/.bashrc

source ~/.bashrc

echo "source /some_path/py3/bin/activate" > /opt/some_project/.env
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
requests 检查状态码
```



```
pip install pipreqs
pipreqs ./ --force
```