cd ..
cd ..

python -m pipenv --rm
python -m pipenv --three
python -m pipenv run pip install pip==18.0
python -m pipenv run pip -V

python -m pipenv install cx_freeze==5.1.1
