.SILENT:

NAMESPACE = $(shell yq '.namespace' galaxy.yml)
COLLECTION = $(shell yq '.name' galaxy.yml)
VERSION = $(shell yq '.version' galaxy.yml)

########
# Lint #
########

## Lint - Lint collection [VERBOSE]
lint:
	ansible-lint \
		$(if $(VERBOSE), -v) \
		--force-color
.PHONY: lint

########
# Test #
########

## Test - Run all collection tests (but doc and coverage)
test: test.sanity test.units test.integration
.PHONY: test

## Test - Run collection sanity tests [VERBOSE]
test.sanity:
	ansible-test sanity \
		--python 3.13 \
		$(if $(VERBOSE), --verbose) \
		--color yes
.PHONY: test.sanity

## Test - Run collection units tests [VERBOSE|COVERAGE]
test.units:
	ansible-test units \
		--python 3.13 \
		--venv \
		$(if $(VERBOSE), --verbose) \
		$(if $(COVERAGE), --coverage) \
		--color yes
.PHONY: test.units

## Test - Run collection integration tests [VERBOSE|COVERAGE]
test.integration:
	ansible-test integration \
		$(if $(VERBOSE), --verbose) \
		$(if $(COVERAGE), --coverage) \
		--color yes
.PHONY: test.integration

## Test - Run collection documentation tests [VERBOSE]
test.doc:
	$(foreach type,module filter, \
		$(foreach plugin,$(shell ansible-doc --list $(NAMESPACE).$(COLLECTION) --type $(type) --json | jq --raw-output 'keys[]'), \
			ansible-doc \
				$(if $(VERBOSE), --verbose) \
				--type $(type) \
				$(plugin) > /dev/null && \
		) \
	) true
.PHONY: test.doc

## Test - Run collection coverage [VERBOSE]
test.coverage:
	ansible-test coverage xml \
		--requirements \
		--venv \
		--python 3.13 \
		--group-by command \
		--group-by version \
		$(if $(VERBOSE), --verbose) \
		--color yes
.PHONY: test.coverage

###################
# Build / Publish #
###################

## Build - Build collection [VERBOSE]
build:
	ansible-galaxy collection build \
		--output-path build \
		--force \
		$(if $(VERBOSE), --verbose)
		
.PHONY: build
