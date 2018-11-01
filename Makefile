install:
	pip install -r requirements.txt
lint:
	pylint ./habroproxy
test:
	pytest
run:
	python run.py
