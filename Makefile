# Variables
PYTHON := poetry run python
PYTEST := poetry run pytest
RUFF := poetry run ruff format
FIND := find

# Directories
SRC_DIR := ./aiohttp_extracts
TEST_DIR := ./tests

# Targets
.PHONY: clean test run



#Format the files
format:
	$(RUFF) $(SRC_DIR)

# Clean target to delete __pycache__ directories
clean:
	$(FIND) . -type d -name "__pycache__" -exec rm -rf {} +

# Test target to run pytest with specified options
test:
	$(PYTEST) $(TEST_DIR) -vv -s --showlocals

coverage:
	$(PYTEST) $(TEST_DIR) --cov --cov-report=html:coverage