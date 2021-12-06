.PHONY: clean
clean:
	find . -name "__pycache__" -type d -exec rm -r -- '{}' +
	find . -name "*.egg-info" -type d -exec rm -r -- '{}' +

.PHONY: test
test:
	pytest -vv --durations=0

.PHONY: format
format:
	black --target-version py310 .

