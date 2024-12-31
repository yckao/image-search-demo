from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse

from src.dependencies import (
    get_clip_service,
    get_database,
    get_default_storage_provider,
    get_storage_service,
)
from src.exceptions import ServiceException
from src.image.router import router as image_router
from src.storage.router import router as storage_router

app = FastAPI(
    responses={
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "INTERNAL_SERVER_ERROR",
                        "detail": "Internal server error",
                    }
                }
            },
        },
    },
)

app.include_router(
    prefix="/images",
    router=image_router,
    dependencies=[
        Depends(get_database),
        Depends(get_clip_service),
        Depends(get_default_storage_provider),
    ],
)

app.include_router(
    prefix="/storage/{provider_name}",
    router=storage_router,
    responses={
        400: {
            "description": "Unsupported storage provider",
            "content": {
                "application/json": {
                    "example": {
                        "error_code": "UNSUPPORTED_STORAGE_PROVIDER",
                        "detail": "Unsupported storage provider",
                    },
                },
            },
        },
    },
    dependencies=[
        Depends(get_storage_service),
    ],
)


@app.exception_handler(ServiceException)
async def validation_exception_handler(_: Request, exc: ServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "error_code": exc.error_code,
                "detail": exc.detail,
            }
        ),
    )


@app.exception_handler(Exception)
async def default_exception_handler(_: Request, exc: Exception):
    e = ServiceException(detail=str(exc))
    return JSONResponse(
        status_code=e.status_code,
        content=jsonable_encoder(
            {
                "error_code": e.error_code,
                "detail": e.detail,
            }
        ),
    )


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
