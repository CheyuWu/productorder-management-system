# productorder-management-system

## How it works
> Connect to localhost:8000/docs
```
$ docker compose up -d
```


## Dev part
### Install environment - Python 3.10
```
$ make install
```

### Activate dev env
```
$ source .venv/bin/activate
```

### update migrations
```
$ alembic revision --autogenerate -m "YOUR_MESSAGE"
$ alembic upgrade head  
```

### Downgrade migrations
```
$ alembic history # check history
$ alembic downgrade XXXX
```

### Generate secret key
```
$ openssl rand -hex 32
```
