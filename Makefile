install:
	pip install -r requirements.txt
lint:
	python -m flake8 ./src
test:
	pytest
run:
	python run.py
