

.PHONY: install dev env db build


# For development
install:
	pip3 install -r requirements.txt
dev:
	uvicorn api:app --host 0.0.0.0 --port 8000 --reload
db:
	docker run --name postgres -e POSTGRES_DB=app \
	-e POSTGRES_USER=dev \
	-e POSTGRES_PASSWORD=password \
	-p 5432:5432 -d postgres

build:
	docker build --tag server:latest . -f Dockerfile

prod:
	docker compose up -d