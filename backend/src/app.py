from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

import logging

from api.v1.routes.addresses import router as address_router
from api.v1.routes.health import router as health_router
from database.base import Base, engine
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from helpers.common_log import CommonLog


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AddressBook",
    summary="A minimal REST API to create, update, delete and query addresses by location.",
    version="v1",
)


@app.exception_handler(Exception)
def handle_internal_server_exception(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    logger.exception(
        CommonLog.UNEXPECTED_ERROR_FOR_ENDPOINT.format(
            method=request.method, path=request.url.path
        )
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": CommonLog.INTERNAL_SERVER_ERROR},
    )


app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(address_router, prefix="/api/v1", tags=["Addresses"])
