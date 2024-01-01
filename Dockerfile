FROM python:3.10.12-slim-buster

COPY . /app
WORKDIR /app
# get cert
RUN pip3 install -r requirements.txt

CMD ["./scripts/start.sh"]