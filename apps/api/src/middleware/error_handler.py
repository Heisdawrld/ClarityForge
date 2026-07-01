import logging
from typing import Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: dict | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            message=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class RateLimitError(AppException):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    correlation_id = getattr(request.state, "correlation_id", None)

    logger.error(
        "app_exception",
        extra={
            "correlation_id": correlation_id,
            "message": exc.message,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "details": exc.details,
                "correlation_id": correlation_id,
            }
        },
    )


async def validation_exception_handler(
    request: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    correlation_id = getattr(request.state, "correlation_id", None)

    errors = []
    if isinstance(exc, RequestValidationError):
        errors = [
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]
    elif isinstance(exc, ValidationError):
        errors = [
            {
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]

    logger.warning(
        "validation_error",
        extra={
            "correlation_id": correlation_id,
            "errors": errors,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation error",
                "details": {"errors": errors},
                "correlation_id": correlation_id,
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    correlation_id = getattr(request.state, "correlation_id", None)

    logger.exception(
        "unhandled_exception",
        extra={
            "correlation_id": correlation_id,
            "error": str(exc),
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "correlation_id": correlation_id,
            }
        },
    )


def add_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
