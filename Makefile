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
  VIZ_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(VIZ_ARGS):;@:)
endif
ifeq (generate,$(firstword $(MAKECMDGOALS)))
  GENERATE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(GENERATE_ARGS):;@:)
endif
ifeq (bench,$(firstword $(MAKECMDGOALS)))
  BENCH_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(BENCH_ARGS):;@:)
endif

venv/bin/activate: requirements.txt
	@echo "================="
	@echo "Installing packages..."
	python -m venv venv
	source venv/bin/activate && venv/bin/pip install -r requirements.txt
	@echo "Packages successfully installed"
	@echo "================="

install: venv/bin/activate

run : install
	@echo "================="
	@echo "Generating a solution using polywriter..."
	source venv/bin/activate && python src/polywriter.py $(RUN_ARGS)
	@echo "Solutions completed"
	@echo "================="

generate: install
	@echo "================="
	@echo "Generating every solutions..."
	source venv/bin/activate && python src/polyhash.py $(GENERATE_ARGS)
	@echo "Solutions generated"
	@echo "================="

lint: install
	@echo "================="
	@echo "Looking for linting and formating errors using flake8 and pep8 rules..."
	source venv/bin/activate && flake8 src --ignore=F401,W503,W292 && pycodestyle src --ignore=W503,W292
	@echo "No rule violations found, code should be pretty enough :D"
	@echo "================="

tests: install
	@echo "================="
	@echo "Launching tests..."
	source venv/bin/activate && python src/polytests.py
	@echo "Success"
	@echo "================="

viz: install
	@echo "================="
	@echo "Launching visualization..."
	source venv/bin/activate && python src/polyvisualizer.py $(VIZ_ARGS)
	@echo "Success"
	@echo "================="

bench: install
	@echo "================="
	@echo "Launching benchmarks..."
	source venv/bin/activate && python src/polybench.py $(BENCH_ARGS)
	@echo "Success"
	@echo "================="

all: install lint tests

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








































































































































cuphead: install
	@cat src/Objects/.cup
