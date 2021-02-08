.PHONY: test run clean lint


all: lint-js


test: test-unit

test-unit:
	yarn run test:unit

# test-with-coverage:
# 	yarn run test-with-coverage
#


run:
	yarn serve

clean:
	rm -rf node_modules dist tmp coverage yarn-error.log

rebuild: clean
	yarn
	make build

build:
	yarn run build

# consistent name with other projects.
lint: lint-js

lint-js:
	yarn run prettier -l src *.js .*.js
	yarn run lint

lint-ts:
	npx tsc

format:
	yarn run prettier --write src *.js .*.js
