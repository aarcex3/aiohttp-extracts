# Variables
PYTHON := poetry run python
PYTEST := poetry run pytest
RUFF := poetry run ruff format
FIND := find

# Directories
SRC_DIR := ./aiohttp_extracts
TEST_DIR := ./tests
COVERAGE_DIR := ./coverage

# Targets
.PHONY: clean test run format coverage


format:
	$(RUFF) $(SRC_DIR)
	$(RUFF) $(TEST_DIR)


clean:
	$(FIND) . -type d -name "__pycache__" -exec rm -rf {} +
	-rm -rf $(COVERAGE_DIR)

test:
	$(PYTEST) $(TEST_DIR) -vv -s --showlocals

coverage:
	-rm -rf $(COVERAGE_DIR)
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html:$(COVERAGE_DIR)
