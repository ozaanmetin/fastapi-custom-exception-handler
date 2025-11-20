from fastapi import FastAPI, Path

from exceptions import (
    ApiException,
    BookAlreadyExistsException,
    BookNotFoundException,
    InvalidBookDataException,
    UnauthorizedException,
)
from handlers.exception_handler import api_exception_handler

app = FastAPI(title="Custom Exception Handler Demo")

# Register the custom exception handler
app.add_exception_handler(ApiException, api_exception_handler)

# In-memory database for demo purposes
books_db = {
    1: {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    2: {"id": 2, "title": "1984", "author": "George Orwell"},
    3: {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Custom Exception Handler Demo API"}


@app.get("/books")
async def get_books():
    """Get all books."""
    return {"books": list(books_db.values())}


@app.get("/books/{book_id}")
async def get_book(book_id: int = Path(..., description="The ID of the book")):
    """
    Get a specific book by ID.

    Raises BookNotFoundException if book doesn't exist.
    """
    if book_id not in books_db:
        raise BookNotFoundException(book_id=book_id)

    return {"book": books_db[book_id]}


@app.post("/books")
async def create_book(title: str, author: str):
    """
    Create a new book.

    Raises:
        InvalidBookDataException: If title or author is empty
        BookAlreadyExistsException: If book with same title already exists
    """
    # Validate input
    if not (3 <= len(title.strip()) <= 100):
        raise InvalidBookDataException(
            detail="Title and author are required",
            validation_errors={
                "title": "Title must be between 3 and 100 characters long"
            },
        )

    # Check if book already exists
    for book in books_db.values():
        if book["title"].lower() == title.lower():
            raise BookAlreadyExistsException(book_title=title)

    # Create new book
    new_id = max(books_db.keys()) + 1 if books_db else 1
    new_book = {"id": new_id, "title": title, "author": author}
    books_db[new_id] = new_book

    return {"message": "Book created successfully", "book": new_book}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(..., description="The ID of the book")):
    """
    Delete a book by ID.

    Raises BookNotFoundException if book doesn't exist.
    """
    if book_id not in books_db:
        raise BookNotFoundException(book_id=book_id)

    deleted_book = books_db.pop(book_id)
    return {"message": "Book deleted successfully", "book": deleted_book}


@app.get("/protected")
async def protected_endpoint():
    """
    Example of a protected endpoint.

    Always raises UnauthorizedException for demonstration.
    """
    raise UnauthorizedException(detail="Please provide valid authentication credentials")


@app.get("/custom-error")
async def custom_error_endpoint():
    """
    Example of raising ApiException with custom attributes.
    """
    raise ApiException(
        status_code=418,
        detail="I'm a teapot",
        error_code="TEAPOT",
        data={"info": "This server refuses to brew coffee because it is a teapot"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
