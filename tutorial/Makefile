.PHONY: clean clean-test clean-pyc clean-build clean-tooling help
.DEFAULT_GOAL := help
STAGE=dev

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-tooling ## remove all build, test, coverage and Python artifacts

clean-tooling: ## removes node_modules and .venv
	rm -rf node_modules/
	rm -rf .venv/

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 tutorial tests

test: ## run tests quickly with the default Python
	py.test -v

test-all: create-venv ## run tests on every Python version with tox
	pipenv run tox

coverage: ## check code coverage quickly with the default Python
	coverage run -m pytest -v
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

create-venv: ## setup virtual env for project in .venv if it does not exist
	set -eux pipefail
	if [ ! -d ".venv" ]; then \
		export PIPENV_IGNORE_VIRTUALENVS=1, PIPENV_VENV_IN_PROJECT=1 && pipenv lock && pipenv sync --dev; \
	fi

setup: create-venv ## setup serverless (node) and create a .venv
	set -eux pipefail
	npm install

deploy-model: ## deploy model to s3
	./training/deploy_model.sh

deploy: ## deploy serverless project to dev
	./node_modules/serverless/bin/serverless deploy --stage=$(STAGE)

remove: ## remove the stack deployed with serverless
	./node_modules/serverless/bin/serverless remove --stage=$(STAGE)


