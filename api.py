from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from db.database import init_db, engine
from routes import product, user

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


@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    logging.error(exc)
    err_msg = f"{request.url}: {str(exc)}"
    logging.error(err_msg)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        content={"message": err_msg}
    )


# app.include_router(login)
app.include_router(user.router)
app.include_router(product.router)
