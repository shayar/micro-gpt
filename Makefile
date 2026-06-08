# Convenience commands. Docker Compose is still the source of truth.

.PHONY: run run-inference down test smoke secret

run:
	docker compose up --build api qdrant redis searxng

run-inference:
	docker compose --profile inference up --build

down:
	docker compose down

test:
	cd api && pip install -r requirements-dev.txt && pytest

smoke:
	bash scripts/smoke_test.sh

secret:
	python scripts/generate_secret.py
