# FastAPI Custom Exception Handler

A comprehensive example of implementing custom exception handling in FastAPI with a base `ApiException` class that can be extended for specific error types.

## Features

- **Base ApiException class** with customizable attributes:
  - `status_code`: HTTP status code
  - `detail`: Error message
  - `error_code`: Application-specific error code
  - `headers`: Optional response headers
  - `data`: Additional error data (e.g., validation errors)

- **Custom exception handler** that catches all `ApiException` instances and returns proper JSON responses

- **Example exceptions**:
  - `BookNotFoundException` (404)
  - `BookAlreadyExistsException` (409)
  - `InvalidBookDataException` (422)
  - `UnauthorizedException` (401)
  - `ForbiddenException` (403)
  - `BadRequestException` (400)
  - `InternalServerException` (500)


## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app/main.py
```

The API will be available at `http://localhost:8000`\
Swagger will be available at `http://localhost:8000/docs`

## Usage Examples

### Creating Custom Exceptions

#### Simple exception with default values:
```python
from app.exceptions import BookNotFoundException

raise BookNotFoundException(book_id=123)
# Response: {"detail": "Book with ID 123 not found", "error_code": "book_not_found"}
```

#### Exception with custom detail:
```python
from app.exceptions import UnauthorizedException

raise UnauthorizedException(detail="Invalid token provided")
# Response: {"detail": "Invalid token provided", "error_code": "unauthorized"}
```

#### Exception with validation errors:
```python
from app.exceptions import InvalidBookDataException

raise InvalidBookDataException(
    detail="Validation failed",
    validation_errors={
        "title": "Title must be at least 3 characters",
        "author": "Author is required"
    }
)
# Response includes validation_errors in data field
```


### Creating Your Own Exception Types

```python
from app.exceptions.base import ApiException

class UserNotFoundException(ApiException):
    status_code = 404
    detail = "User not found"
    error_code = "user_not_found"

    def __init__(self, user_id: int = None, **kwargs):
        if user_id:
            kwargs['detail'] = f"User with ID {user_id} not found"
        super().__init__(**kwargs)
```

## Testing the API

### Get a book (success):
```bash
curl http://localhost:8000/books/1
```

### Get a non-existent book (error):
```bash
curl http://localhost:8000/books/999
# Returns: {"detail": "Book with ID 999 not found", "error_code": "book_not_found"}
```

### Create a book with invalid data:
```bash
curl -X POST "http://localhost:8000/books?title=&author="
# Returns validation error with details
```

### Create a duplicate book:
```bash
curl -X POST "http://localhost:8000/books?title=1984&author=George%20Orwell"
# Returns: {"detail": "Book with title '1984' already exists", "error_code": "book_already_exists"}
```

## Response Format

All API exceptions return a consistent JSON structure:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "data": {
    "additional": "context"
  }
}
```

The `error_code` and `data` fields are optional and only included if set.

