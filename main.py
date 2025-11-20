from fastapi import FastAPI, Path

from exceptions import ApiException, UnauthorizedException
from exception_handler import api_exception_handler
from services import BookService

app = FastAPI(title="Custom Exception Handler Demo")

# Register the custom exception handler
app.add_exception_handler(ApiException, api_exception_handler)

# In-memory database for demo purposes
books_db = {
    1: {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    2: {"id": 2, "title": "1984", "author": "George Orwell"},
    3: {"id": 3, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
}

# Initialize book service
book_service = BookService(books_db)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Custom Exception Handler Demo API"}


@app.get("/books")
async def get_books():
    """Get all books."""
    books = book_service.get_all_books()
    return {"books": books}


@app.get("/books/{book_id}")
async def get_book(book_id: int = Path(..., description="The ID of the book")):
    """
    Get a specific book by ID.

    Raises BookNotFoundException if book doesn't exist.
    """
    book = book_service.get_book_by_id(book_id)
    return {"book": book}


@app.post("/books")
async def create_book(title: str, author: str):
    """
    Create a new book.

    Raises:
        InvalidBookDataException: If title or author is empty
        BookAlreadyExistsException: If book with same title already exists
    """
    new_book = book_service.create_book(title=title, author=author)
    return {"message": "Book created successfully", "book": new_book}


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(..., description="The ID of the book")):
    """
    Delete a book by ID.

    Raises BookNotFoundException if book doesn't exist.
    """
    deleted_book = book_service.delete_book(book_id)
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
