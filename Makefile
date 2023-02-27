.PHONY: dependencies
pip-install:
	pip install -r requirements.txt

.PHONY: docker
docker-start:
	docker-compose up

.PHONY: postgres
	psql -d postgres -U postgres -p 5432 -h localhost -f alter_table.sql

.PHONY: python
run-code:
	python run.py