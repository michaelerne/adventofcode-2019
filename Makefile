.PHONY: help lint run

DIR = .

.DEFAULT: help
help:
	@echo "make lint"
	@echo "       run mypy and pylint"
	@echo "make run"
	@echo "       run all days"


lint:
	$(foreach file, $(wildcard $(DIR)/*.py), python -m mypy $(file);)
	$(foreach file, $(wildcard $(DIR)/*.py), python -m pylint $(file);)

run:
	$(foreach file, $(wildcard $(DIR)/day_*.py), python $(file);)
