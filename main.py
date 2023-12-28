from fastapi import FastAPI
from db import models
from db.database import SessionLocal, engine

# from routes import login, orders, product

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    """
    Create db connection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# app.include_router(login)
# app.include_router(login)
