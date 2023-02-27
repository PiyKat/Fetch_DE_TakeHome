.PHONY: dependencies
pip-install:
	pip install -r requirements.txt

.PHONY: docker
docker-start:
	docker-compose up -d
docker-stop:
	docker-compose down --remove-orphans

.PHONY: postgres
alter-table:
	psql -d postgres -U postgres -p 5432 -h localhost -f ./scripts/alter_table.sql

.PHONY: python
run:
	python run.py