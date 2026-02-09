.PHONY: install dev-install run test lint format clean

# Install production dependencies
install:
	pip install -r requirements.txt

# Install with development dependencies
dev-install:
	pip install -r requirements.txt
	pre-commit install

# Run the Streamlit app
run:
	streamlit run app/main.py

# Run tests with coverage
test:
	pytest tests/ -v --cov=app --cov=modules --cov-report=term-missing

# Run linting
lint:
	flake8 app/ modules/ tests/
	black --check app/ modules/ tests/
	isort --check-only app/ modules/ tests/

# Format code
format:
	black app/ modules/ tests/
	isort app/ modules/ tests/

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/

# Setup development environment
setup:
	python -m venv venv
	. venv/Scripts/activate && pip install -r requirements.txt
	pre-commit install

# Help
help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev-install  - Install with dev tools + pre-commit"
	@echo "  make run          - Run Streamlit app"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Check code style"
	@echo "  make format       - Format code with black/isort"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make setup        - Full dev environment setup"
