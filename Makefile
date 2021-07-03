.PHONY:

build:
	python3 -m build

clean:
	rm -rf dist
	rm -rf build

test:
	python3 -m twine upload --repository testpypi dist/*

publish:
	python3 -m twine upload dist/*
