all : build test


build : ./setup.py
	python $< build

test :
	find ./tests -type f  | xargs -I file python file

install : ./setup.py
	python setup.py install
