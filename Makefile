.PHONY: migrate
migrate:
	alembic upgrade head


.PHONY: makemigration
makemigration:
	alembic revision --autogenerate -m "${message}"
