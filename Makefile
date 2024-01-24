SHELL := /bin/bash

#https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif
ifeq (viz,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
ifeq (generate,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

ifdef OS
   Source = call venv/Scripts/activate.ps1
else
   ifeq ($(shell uname), Linux)
      Source = source venv/bin/activate
   endif
endif

run : install
	@echo "================="
	@echo "Generating a solution using polywriter..."
	@$(Source)
	python src/polywriter.py $(RUN_ARGS)
	@echo "Solutions completed"
	@echo "================="

venv/bin/activate: requirements.txt
	@echo "================="
	@echo "Installing packages..."
	python -m venv venv
	@$(Source) 
	venv/bin/pip install -r requirements.txt
	@echo "Packages successfully installed"
	@echo "================="

install: 

generate: install
	@echo "================="
	@echo "Generating every solutions..."
	@$(Source) 
	python src/polyhash.py $(RUN_ARGS)
	@echo "Solutions generated"
	@echo "================="

lint: install
	@echo "================="
	@echo "Looking for linting and formating errors using flake8 and pep8 rules..."
	@$(Source) 
	flake8 src --ignore=F401,W503,W292
	pycodestyle src --ignore=W503,W292
	@echo "No rule violations found, code should be pretty enough :D"
	@echo "================="

tests: install
	@echo "================="
	@echo "Launching tests..."
	@$(Source) 
	python src/polytests.py
	@echo "Success"
	@echo "================="

viz: install
	@echo "================="
	@echo "Launching visualization..."
	@$(Source) 
	python src/polyvisualizer.py $(RUN_ARGS)
	@echo "Success"
	@echo "================="

all: lint tests

clean:
	@echo "Cleaning  non-mandatory files..."
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf venv
	rm -f solutions/*.out
	rm -f solutions_theo/*.out
	rm -f solutions_loic/*.out
	rm -f solutions_amedeo/*.out
	@echo "Success"
