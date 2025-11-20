# FastAPI Custom Exception Handler

A simple example of implementing custom exception handling in FastAPI using a base `ApiException` class.

## Overview

This project demonstrates how to create a unified exception handling system in FastAPI. Instead of manually handling errors throughout your code, you define custom exceptions that inherit from a base `ApiException` class, and a single exception handler catches and formats all of them consistently.

### Core Components

**ApiException** - Base exception class with:
- `status_code`: HTTP status code (e.g., 404, 409, 422)
- `detail`: Error message
- `error_code`: Machine-readable error identifier
- `data`: Additional context (like validation errors)

**Exception Handler** - Catches all `ApiException` instances and returns a consistent JSON response format.

**Service Layer** - A basic example of business logics which we throw api exceptions in exceptional cases, keeping endpoints clean.

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## How It Works

### 1. Define Custom Exceptions

```python
class BookNotFoundException(ApiException):
    status_code = 404
    error_code = "book_not_found"

    def __init__(self, book_id: int = None, **kwargs):
        if book_id:
            kwargs['detail'] = f"Book with ID {book_id} not found"
        super().__init__(**kwargs)
```

### 2. Throw Exceptions in Service Layer

```python
class BookService:
    def get_book_by_id(self, book_id: int) -> dict:
        if book_id not in self.books_db:
            raise BookNotFoundException(book_id=book_id)
        return self.books_db[book_id]
```

### 3. Exception Handler Formats Response

The handler automatically catches these exceptions and returns:

```json
{
  "detail": "Book with ID 999 not found",
  "error_code": "book_not_found"
}
```

## Example Exceptions

- `BookNotFoundException` - 404, book not found
- `BookAlreadyExistsException` - 409, duplicate book
- `InvalidBookDataException` - 422, validation errors
- `UnauthorizedException` - 401, authentication required
- `BadRequestException` - 400, invalid request
- `InternalServerException` - 500, server error

## Testing

```bash
# Get non-existent book
curl http://localhost:8000/books/999

# Create duplicate book
curl -X POST "http://localhost:8000/books?title=1984&author=George%20Orwell"

# Invalid data
curl -X POST "http://localhost:8000/books?title=AB&author=Someone"
```

## Response Format

```json
{
  "detail": "Error message",
  "error_code": "error_identifier",
  "data": {
    "validation_errors": {
      "field": "error details"
    }
  }
}
```

The `error_code` and `data` fields are optional.
