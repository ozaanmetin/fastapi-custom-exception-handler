from typing import Any, Optional
from exceptions.base import ApiException


class BookNotFoundException(ApiException):
    """Exception raised when a book is not found."""

    status_code = 404
    detail = "Book not found"
    error_code = "book_not_found"

    def __init__(
        self,
        book_id: Optional[int] = None,
        detail: Optional[str] = None,
        **kwargs,
    ):
        if book_id and not detail:
            detail = f"Book with ID {book_id} not found"

        super().__init__(detail=detail, **kwargs)


class BookAlreadyExistsException(ApiException):
    """Exception raised when trying to create a book that already exists."""

    status_code = 409
    detail = "Book already exists"
    error_code = "book_already_exists"

    def __init__(
        self,
        book_title: Optional[str] = None,
        detail: Optional[str] = None,
        **kwargs,
    ):
        if book_title and not detail:
            detail = f"Book with title '{book_title}' already exists"

        super().__init__(detail=detail, **kwargs)


class InvalidBookDataException(ApiException):
    """Exception raised when book data is invalid."""

    status_code = 422
    detail = "Invalid book data"
    error_code = "invalid_book_data"

    def __init__(
        self,
        validation_errors: Optional[dict[str, Any]] = None,
        detail: Optional[str] = None,
        **kwargs,
    ):
        data = kwargs.pop("data", None) or {}
        if validation_errors:
            data["validation_errors"] = validation_errors

        super().__init__(detail=detail, data=data, **kwargs)


class UnauthorizedException(ApiException):
    """Exception raised when user is not authenticated."""

    status_code = 401
    detail = "Authentication required"
    error_code = "unauthorized"
    headers = {"WWW-Authenticate": "Bearer"}


class ForbiddenException(ApiException):
    """Exception raised when user doesn't have permission."""

    status_code = 403
    detail = "You don't have permission to access this resource"
    error_code = "forbidden"


class BadRequestException(ApiException):
    """Exception raised for bad requests."""

    status_code = 400
    detail = "Bad request"
    error_code = "bad_request"


class InternalServerException(ApiException):
    """Exception raised for internal server errors."""

    status_code = 500
    detail = "Internal server error"
    error_code = "internal_server_error"
