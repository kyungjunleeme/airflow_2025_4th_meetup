.PHONY: venv install run test clean

venv:
	uv venv

install:
	uv pip install -e .
	uv pip install pytest

run:
	airflow-compat-demo

test:
	pytest

clean:
	rm -rf .venv __pycache__ .pytest_cache dist build *.egg-info
