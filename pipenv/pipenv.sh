
# export PIPENV_VENV_IN_PROJECT=1
python -m pipenv --rm

# 备份
mv Pipfile Pipfile.bak
rm -rf Pipfile.lock

# 删除环境
python -m pipenv --rm
python -m pipenv clean
# python -m pipenv install --skip-lock

# 更新pip
# python -m pipenv shell
python -m pipenv install pip==18.0 --skip-lock
python -m pipenv install setuptools==19.2.0 --skip-lock

# 安装cx_freeze
python -m pipenv install cx_freeze==5.1.1

# 恢复
mv Pipfile.bak Pipfile
rm -rf Pipfile.lock

python -m pipenv install --skip-lock
python -m pipenv install gunicorn==19.9.0 --skip-lock
python -m pipenv install gevent==1.4.0 --skip-lock
python -m pipenv graph
