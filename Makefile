.PHONY: install project build publish clean install-local

install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run --build

install-local:
	python3 -m pip install dist/*.whl

clean:
	rm -rf dist build *.egg-info
	find. -name "__pycache__" -type d -exec rm -rf {} +
