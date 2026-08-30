.ONESHELL:
.PHONY: docs

build_dir := build
venv_dir := venv
docs_dir := docs

enter_venv := . "$(venv_dir)/bin/activate"

build: venv
	$(enter_venv)
	python -m pip install --upgrade build hatchling
	python -m build

publish: build
	$(enter_venv)
	python -m pip install --upgrade twine
	python -m twine upload --repository pypi dist/*

docs: venv
	$(enter_venv)
	python -m pip install --group docs .
	sphinx-build "$(docs_dir)" "$(docs_dir)/$(build_dir)"

venv:
	python -m venv "$(venv_dir)"
	$(enter_venv)
	python -m pip install --upgrade pip
	python -m pip install .

clean:
	rm -rf dist
	rm -rf "$(docs_dir)/$(build_dir)"
	rm -rf "$(venv_dir)"
