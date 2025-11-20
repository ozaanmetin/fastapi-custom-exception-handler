from typing import Any, Optional


class ApiException(Exception):
    """
    Base API exception class that all custom exceptions should inherit from.

    status_code: HTTP status code to return
    detail: Error message or detail
    headers: Optional headers to include in response
    error_code: Optional application-specific error code
    data: Optional additional data to include in response
    """

    status_code: int = 500
    detail: str = "Internal server error"
    headers: Optional[dict[str, Any]] = None
    error_code: Optional[str] = None
    data: Optional[dict[str, Any]] = None

    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: Optional[int] = None,
        headers: Optional[dict[str, Any]] = None,
        error_code: Optional[str] = None,
        data: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize the exception with optional overrides.
        
        detail: Override the default detail message
        status_code: Override the default status code
        headers: Override the default headers
        error_code: Override the default error code
        data: Override the default additional data
        """
        if detail is not None:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code
        if headers is not None:
            self.headers = headers
        if error_code is not None:
            self.error_code = error_code
        if data is not None:
            self.data = data

        super().__init__(self.detail)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for JSON response."""
        
        response = {
            "detail": self.detail,
        }

        if self.error_code:
            response["error_code"] = self.error_code

        if self.data:
            response["data"] = self.data

        return response
