.PHONY: test

test:
	pytest -xvs --disable-warnings tests/test.py
	pytest -xvs --disable-warnings tests/nongithubtest.py
	ls
	rm "./test.yml"

profile:
	rm -f profile_output.txt
	rm -f main.py.lprof
	kernprof -l main.py --catalog bluesky-tutorial-BMM --search "time"
	python3 -m line_profiler main.py.lprof > profile_output.txt
