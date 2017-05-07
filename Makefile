PYTHON = python3
CHECKSTYLE = flake8
PYTHON_FILES = $(shell find data_mapper -type f -name "*.py")

all: test checkstyle

test: doctest unittest

doctest:
	@echo "Running doctest"
	@$(PYTHON) -m doctest $(PYTHON_FILES)

unittest:
	@echo "Running unittest"
	@$(PYTHON) -m unittest discover -s data_mapper/test/ -p test*.py

checkstyle:
	@echo "Running checkstyle"
	@$(CHECKSTYLE) $(PYTHON_FILES)

clean:
	@find . -name "*.pyc" -exec rm -f {} \;
	@find . -name "__pycache__" -exec rm -f {} \;