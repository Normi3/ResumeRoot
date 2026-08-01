VENV := .venv
PYTHON := $(VENV)/bin/python
APPLYPILOT := $(VENV)/bin/applypilot
RESUMEROOT := $(VENV)/bin/resumeroot

.PHONY: bootstrap init doctor status run apply test

bootstrap:
	./scripts/bootstrap.sh

init:
	$(RESUMEROOT) init
	$(APPLYPILOT) init

doctor:
	$(RESUMEROOT) doctor
	$(APPLYPILOT) doctor

status:
	$(RESUMEROOT) status

run:
	$(APPLYPILOT) run $(ARGS)

apply:
	$(APPLYPILOT) apply $(ARGS)

test:
	$(PYTHON) -m unittest discover -s tests -v
