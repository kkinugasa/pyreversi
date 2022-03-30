PACKAGE := $$(sed -n 's/name = "\(.*\)"/\1/p' pyproject.toml)
VERSION := $$(sed -n 's/__version__ = "\(.*\)"/\1/p' $(PACKAGE)/_version.py )

# It is better to set the value 1.
export DOCKER_CONTENT_TRUST = 1
export DOCKER_BUILDKIT = 1

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | \
		awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {\
			split(\$$1,A,/ /);for(i in A)print A[i]\
		}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

setup:
	@poetry install

clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

env-clean: clean
	@rm -rf .venv
	@rm -rf .tox

format:
	@poetry run isort .
	@poetry run black .

lint:
	@poetry run pylint -d C $(PACKAGE)
	@poetry run mypy .

# GitHub dependency graph does not support poetry.lock
# https://docs.github.com/en/code-security/supply-chain-security/about-the-dependency-graph#supported-package-ecosystems
requirements:
	@poetry export --without-hashes -f requirements.txt -o requirements.txt

test:
	@poetry run pytest

version:
	@sed -n 's/version = \(.*\)/__version__ = \1/p' pyproject.toml > $(PACKAGE)/_version.py

pre-commit: requirements version format lint test

# CIS-DI-0005: DOCKER CONTENT TRUST
# CIS-DI-0006: HEALTHCHECK
docker:
	@hadolint Dockerfile
	@docker build -t $(PACKAGE):$(VERSION) .
	@sudo dockle --exit-code 1 --exit-level info --ignore CIS-DI-0006 --ignore CIS-DI-0005 $(PACKAGE):$(VERSION)
	@trivy image --clear-cache
	@trivy image --exit-code 1 --ignore-unfixed $(PACKAGE):$(VERSION)

# run tests against all supported python versions
tox:
	@tox
