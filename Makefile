SHELL = /bin/bash

venv/bin/activate: requirements.txt
	@echo "Installing packages..."
	python3 -m venv venv
	@source venv/bin/activate
	venv/bin/pip install -r requirements.txt
	@echo "Packages successfully installed"

generate_naive_loic: venv/bin/activate
	@echo "Generating every solutions using naive_loic..."
	@source venv/bin/activate
	python3 src/polyhash.py naive_loic
	@echo "Solutions generated successfully using naive_loic"

generate_naive_theo: venv/bin/activate
	@echo "Generating every solutions using naive_theo..."
	@source venv/bin/activate
	python3 src/polyhash.py naive_theo
	@echo "Solutions generated successfully using naive_theo"

generate_naive_amedeo: venv/bin/activate
	@echo "Generating every solutions using naive_amedeo..."
	@source venv/bin/activate
	python3 src/polyhash.py naive_amedeo
	@echo "Solutions generated successfully using naive_amedeo"

lint: venv/bin/activate
	@echo "Looking for linting and formating errors using flake8 and pep8 rules..."
	@source venv/bin/activate
	flake8 src --ignore=F401,W503,W292
	pycodestyle src --ignore=W503,W292
	@echo "No rule violations found, code should be pretty enough :D"

tests: venv/bin/activate
	@echo "Launching tests..."
	@source venv/bin/activate
	python3 src/polytests.py
	@echo "Success"


clean:
	@echo "Cleaning  non-mandatory files..."
	rm -rf __pycache__
	rm -rf venv
	rm -f solutions/*
	echo "Success"