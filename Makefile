PYTHON ?= python

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install       Install all dependencies (including dev)"
	@echo "  make lint          Run ruff linter"
	@echo "  make format        Run ruff formatter"
	@echo "  make test          Run tests"
	@echo "  make coverage      Run tests with coverage report"
	@echo "  make pre-commit    Install and run pre-commit hooks"
	@echo "  make run-pipeline  Run data pipeline"
	@echo "  make run-api       Start FastAPI server"
	@echo "  make run-streamlit Start Streamlit app"
	@echo "  make docker-up     Start all services with Docker Compose"
	@echo "  make docker-down   Stop Docker Compose services"
	@echo "  make ci            Run full CI locally (lint + test + pipeline + smoke)"

.PHONY: install
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

.PHONY: lint
lint:
	$(PYTHON) -m ruff check app config contracts core pages services tests scripts streamlit_app.py

.PHONY: format
format:
	$(PYTHON) -m ruff format app config contracts core pages services tests scripts streamlit_app.py

.PHONY: test
test:
	$(PYTHON) -m pytest -q

.PHONY: coverage
coverage:
	$(PYTHON) -m pytest --cov=. --cov-report=term-missing --cov-report=html -q
	@echo "HTML report generated at htmlcov/index.html"

.PHONY: pre-commit
pre-commit:
	$(PYTHON) -m pre_commit install
	$(PYTHON) -m pre_commit run --all-files

.PHONY: run-pipeline
run-pipeline:
	$(PYTHON) -m core.pipeline

.PHONY: cli-health
cli-health:
	$(PYTHON) -m core.cli health

.PHONY: cli-validate
cli-validate:
	$(PYTHON) -m core.cli validate

.PHONY: run-api
run-api:
	$(PYTHON) -m uvicorn services.api.main:app --reload

.PHONY: run-streamlit
run-streamlit:
	streamlit run streamlit_app.py

.PHONY: docker-up
docker-up:
	docker compose up --build

.PHONY: docker-down
docker-down:
	docker compose down

.PHONY: ci
ci: lint test
	$(PYTHON) -m core.pipeline
	$(PYTHON) -m core.cli validate
	$(PYTHON) scripts/smoke_api.py
