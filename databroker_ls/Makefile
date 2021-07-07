.PHONY: test

test:
	pytest -xvs --disable-warnings tests/test.py
	pytest -xvs --disable-warnings tests/nongithubtest.py
	rm "databroker-ls/non_existent_file.yml"
	rm "databroker-ls/test.yml"
