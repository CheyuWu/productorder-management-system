from contextlib import asynccontextmanager

from fastapi import FastAPI
from db.database import init_db, engine
from routes import user

# from routes import login, orders, product

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Startup and Shutdown event
    """
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


# app.include_router(login)
app.include_router(user.router)
