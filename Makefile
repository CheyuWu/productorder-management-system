

.PHONY: install dev env makedb


# For development
install:
	pip3 install -r requirements.txt
dev:
	uvicorn api:app --host 0.0.0.0 --port 8000 --reload
makedb:
	docker run --name postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
