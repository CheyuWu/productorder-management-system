from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import init_db

# from routes import login, orders, product


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Startup and Shutdown event
    """
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


# app.include_router(login)
# app.include_router(login)
