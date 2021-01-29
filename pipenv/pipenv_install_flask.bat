@ echo off

:: 打包
python -m pipenv install cx_freeze==5.1.1 --skip-lock
python -m pipenv install gunicorn==19.9.0 --skip-lock
python -m pipenv install gevent==1.4.0 --skip-lock

:: 数据库
python -m pipenv install cx-oracle==6.3.1 --skip-lock
python -m pipenv install sqlalchemy==1.2.0 --skip-lock

:: 网络请求
python -m pipenv install requests==1.2.0 --skip-lock

:: flask相关
python -m pipenv install flask==0.10 --skip-lock
python -m pipenv install flask-cors==2.1.2 --skip-lock
python -m pipenv install flask-restful==0.3.6 --skip-lock
python -m pipenv install flask-sqlalchemy==2.3 --skip-lock

pause