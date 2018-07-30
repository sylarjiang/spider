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