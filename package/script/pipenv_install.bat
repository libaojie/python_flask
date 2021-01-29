@ echo off
cd ..
cd ..

del Pipfile
del Pipfile.lock

python -m pipenv --rm
python -m pipenv install --skip-lock
python -m pipenv run pip install pip==18.0
python -m pipenv run pip -V
python -m pipenv install cx_freeze==5.1.1  --skip-lock


git checkout .
git clean -df
git pull

python -m pipenv install --skip-lock

pasue
