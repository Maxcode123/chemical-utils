CONFIG=./pyproject.toml
PY_FILES:=$(shell find src/chemical_utils -not -path '*/tests/*' -not -name '__init__.py' -name '*.py')

install-documentation-builder:
	$(PIP) install mkdocs mkdocs-material 'mkdocstrings[python]'

start-documentation-server:
	$(INTERPRETER) -m mkdocs serve

deploy-documentation:
	$(INTERPRETER) -m mkdocs gh-deploy --config-file mkdocs.yml

install-package-linter:
	$(PIP) install pylint

install-package-type-checker:
	$(PIP) install mypy

install-package-formatter:
	$(PIP) install black

install-package-builder:
	$(PIP) install --upgrade build

install-package-uploader:
	$(PIP) install --upgrade twine

install-local-package:
	$(PIP) install -e .

install-requirements:
	$(PIP) install typing-extensions property_utils

install-test-requirements:
	$(PIP) install unittest-extensions

test-package:
	$(INTERPRETER) -m unittest discover -v src/chemical_utils/tests/

doctest-package:
	$(INTERPRETER) -m doctest $(PY_FILES)

lint-package:
	$(INTERPRETER) -m pylint --ignore tests --disable C0114,C0301,C0302,W0401,W0614 src/chemical_utils

type-check-package:
	$(INTERPRETER) -m mypy --config-file $(CONFIG) ./src/chemical_utils/

format-package:
	$(INTERPRETER) -m black --config $(CONFIG) ./src/chemical_utils/

build-package:
	$(INTERPRETER) -m build

upload-package:
	$(INTERPRETER) -m twine upload --verbose -u '__token__' dist/*

clean:
	rm -rf dist src/chemical_utils.egg-info