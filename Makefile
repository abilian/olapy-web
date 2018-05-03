.PHONY: test unit full-test clean setup stage deploy


SRC=src
PKG=$(SRC)

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
pip:
	@echo "--> Installing / updating python dependencies for development"
	pip install -q pip-tools
	pip-sync requirements.txt
	pip install -q -r requirements.txt -r dev-requirements.txt
	pip install -e .
	@echo ""
js:
	cd front && yarn

develop: pip js

#
# Linting
#
lint: lint-python lint-js

lint-python:
	@echo "--> Linting Python files"
	flake8 $(SRC)
	@echo "Checking Py3k (basic) compatibility"
	-pylint --rcfile .pylint.rc --py3k *.py $(SRC)
	@echo "Running pylint, some errors reported might be false positives"
	-pylint -E --rcfile .pylint.rc $(SRC)

lint-js:
	cd front && make lint

#
# Running web server
#
run:
	python manage.py


clean:
	find . -name "*.pyc" -delete
	find . -name yaka.db -delete
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

tidy: clean
	rm -rf .tox

format: format-py format-js

format-py:
	isort -rc $(SRC) *.py
	yapf --style google -r -i $(SRC) *.py
	isort -rc $(SRC) *.py

format-js:
	cd front && make format

update-deps:
	pip-compile -U > /dev/null
	pip-compile > /dev/null
	git --no-pager diff requirements.txt

sync-deps:
	pip install -r requirements.txt -r dev-requirements.txt -e .

release:
	git push --tags
	rm -rf /tmp/olapy-web
	git clone . /tmp/olapy-web
	cd /tmp/olapy-web ; python setup.py sdist
	cd /tmp/olapy-web ; python setup.py sdist upload

build:
	cd front && yarn build
	python manage.py

doc:
	cd docs && make html
