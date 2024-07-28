VENV := .venv

setup:
	@python3 -m venv $(VENV)
	@$(VENV)/bin/pip install -r requirements.txt



run:
	@python3 main.py