from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.base import ApiException


async def api_exception_handler(request: Request, exc) -> JSONResponse:
    """
    Custom exception handler for ApiException and its subclasses.

    request: The FastAPI request object
    exc: The ApiException instance that was raised


    returns: JSONResponse with the error details
    """

    if not isinstance(exc, ApiException):
        # If the exception is not an ApiException, re-raise it
        raise JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
        headers=exc.headers,
    )
