.PHONY: help lint test run

DIR = .

.DEFAULT: help
help:
	@echo "make lint"
	@echo "       run mypy and pylint"
	@echo "make test"
	@echo "       run all tests"
	@echo "make run"
	@echo "       run all days"


lint:
	python -m mypy *.py
	python -m pylint --disable=C0114,C0115,C0116,R0801 --max-line-length=120 *.py

test:
	python -m doctest util.py

run:
	$(foreach file, $(wildcard $(DIR)/day_*.py), python $(file);)
