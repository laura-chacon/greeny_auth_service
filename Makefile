SHELL := /bin/bash

test:
	source /home/laura/aws && \
	  python -m testtools.run discover -s tests/
