.PHONY: all default test clean develop lint


SRC=olapy_web
PKG=$(SRC)


all: default

default: test lint


#
# testing
#
test:
	pytest . --durations=10

test-with-coverage:
	pytest --tb=short --cov $(PKG) --cov-report term-missing .

#
# setup
#
develop:
	poetry install
	cd front && yarn


#
# Linting
#
lint: lint-python lint-js

lint-python: lint-flake8 lint-mypy

lint-flake8:
	@echo "--> Linting Python files (with Flake8)"
	flake8 $(SRC)

lint-mypy:
	@echo "--> Typechecking Python files"
	mypy $(SRC)

lint-pylint:
	@echo "Running pylint, some errors reported might be false positives"
	-pylint -E --rcfile .pylint.rc $(SRC)

lint-js:
	cd front && make lint

#
# Running web server
#
build-js:
	cd front && yarn build

run: build-js
	flask run

init:
	flask initdb

clean:
	find . -name "*.pyc" -delete
	find . -name .DS_Store -delete
	find . -name cache -type d -delete
	find . -type d -empty -delete
	rm -f migration.log
	rm -rf build dist
	rm -rf tests/data tests/integration/data
	rm -rf tmp tests/tmp tests/integration/tmp
	rm -rf cache tests/cache tests/integration/cache
	rm -rf *.egg .coverage
	rm -rf doc/_build
	rm -rf static/gen static/.webassets-cache instance/webassets
	rm -rf htmlcov junit-*.xml
	rm -rf .mypy_cache

tidy: clean
	rm -rf .tox
	rm -rf front/dist front/node_modules

format: format-py format-js

format-py:
	black $(SRC) tests *.py
	isort $(SRC) tests *.py

format-js:
	cd front && make format

update-deps:
	poetry update

release:
	poetry publish --build

doc:
	cd docs && make html
