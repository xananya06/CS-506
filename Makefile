# Name of the virtual environment directory
VENV_NAME = .venv

# Default target
.PHONY: all
all: venv install

# Create virtual environment
.PHONY: venv
venv:
	@echo "Creating virtual environment in $(VENV_NAME)..."
	python3 -m venv $(VENV_NAME)

# Install Python dependencies
.PHONY: install
install:
	@echo "Installing dependencies from requirements.txt..."
	$(VENV_NAME)/bin/pip install --upgrade pip
	$(VENV_NAME)/bin/pip install -r requirements.txt

# Activate environment (only for reference)
.PHONY: activate
activate:
	@echo "Run 'source $(VENV_NAME)/bin/activate' to activate the environment"

# Clean environment
.PHONY: clean
clean:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_NAME)
