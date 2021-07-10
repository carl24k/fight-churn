.PHONY:

build:
	python3 -m build

clean:
	rm -rf dist
	rm -rf build
	rm -rf fightchurn.egg-info

test:
	python3 -m twine upload --repository testpypi dist/*

publish:
	python3 -m twine upload dist/*
