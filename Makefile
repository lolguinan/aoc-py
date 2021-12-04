.PHONY: clean
clean:
	find . -name "__pycache__" -type d -exec rm -r -- '{}' +
	find . -name "*.egg-info" -type d -exec rm -r -- '{}' +

