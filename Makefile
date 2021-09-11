.PHONY:

build:
	python3 -m build

clean:
	rm -rf dist
	rm -rf build
	rm -rf fightchurn.egg-info

test:
	pytest tests --verbose

test_verbose:
	pytest tests --verbose --capture=no

publish:
	python3 -m twine upload dist/*
