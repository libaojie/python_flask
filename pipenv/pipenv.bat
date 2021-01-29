@ echo off

:: 移动环境
ren Pipfile Pipfile.bak
del Pipfile.lock


:: 移除环境
python -m pipenv --rm
python -m pipenv clean


:: 更新pip
python -m pipenv run pip install pip==18.0


:: 安装cx_freeze
python -m pipenv install cx_freeze==5.1.1 --skip-lock


:: 恢复
del Pipfile
del Pipfile.lock
ren Pipfile.bak Pipfile
python -m pipenv install --skip-lock
python -m pipenv graph

pause