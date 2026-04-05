PYTHON ?= python

.PHONY: test
test:
	$(PYTHON) -m pytest -q

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
	streamlit run app/streamlit_app.py
