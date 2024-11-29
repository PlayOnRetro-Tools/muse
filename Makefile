.PHONY: help install clean build run lint resources test dist

PYTHON := python
POETRY := poetry
PYRCC := pyrcc5
QRC_DIR := resources
QRC_FILES := $(wildcard $(QRC_DIR)/*.qrc)
PY_RESOURCES := $(QRC_FILES:$(QRC_DIR)/%.qrc=musa/resources/%.py)

help:
	@echo "Available tagets:"
	@echo " install     - Install project dependencies"
	@echo " clean		- Remove build artifacts and cached files"
	@echo " build		- Build the application"
	@echo " run 		- Run the application locally"
	@echo " lint		- Format the code"
	@echo " resources 	- Compile .qrc files to python"
	@echo " test 		- Run tests"

install:
	$(POETRY) install --with dev
	$(POETRY) run pre-commit install

clean:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete

build: clean resources
	@$(POETRY) run pyinstaller --clean musa.spec

run:
	@$(POETRY) run python -m musa

lint:
	@$(POETRY) run black .
	@$(POETRY) run isort .

test:
	@$(POETRY) run pytest

resources: $(PY_RESOURCES)

musa/resources/%.py: $(QRC_DIR)/%.qrc
	@mkdir -p musa/resources
	@$(POETRY) run $(PYRCC) $< -o $@
