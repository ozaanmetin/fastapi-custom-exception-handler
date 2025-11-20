"""
Book service layer for handling business logic and data operations.

This module separates business logic from API endpoints, making the code
more maintainable and testable.
"""

from typing import Dict, List

from exceptions import (
    BookAlreadyExistsException,
    BookNotFoundException,
    InvalidBookDataException,
)


class BookService:
    """Service class for book-related operations."""

    def __init__(self, books_db: Dict[int, dict]):
        self.books_db = books_db

    def get_all_books(self) -> List[dict]:
        """Retrieve all books."""
        return list(self.books_db.values())

    def get_book_by_id(self, book_id: int) -> dict:
        """Retrieve a book by its ID."""
        if book_id not in self.books_db:
            raise BookNotFoundException(book_id=book_id)

        return self.books_db[book_id]

    def create_book(self, title: str, author: str) -> dict:
        """Create a new book."""
        # Validate title length
        if not (3 <= len(title.strip()) <= 100):
            raise InvalidBookDataException(
                detail="Title validation failed",
                validation_errors={
                    "title": "Title must be between 3 and 100 characters long"
                },
            )

        # Validate author
        if not author or not author.strip():
            raise InvalidBookDataException(
                detail="Author validation failed",
                validation_errors={"author": "Author cannot be empty"},
            )

        # Check if book with same title already exists
        for book in self.books_db.values():
            if book["title"].lower() == title.strip().lower():
                raise BookAlreadyExistsException(book_title=title)

        # Create new book
        new_id = max(self.books_db.keys()) + 1 if self.books_db else 1
        new_book = {"id": new_id, "title": title.strip(), "author": author.strip()}
        self.books_db[new_id] = new_book
        return new_book

    def delete_book(self, book_id: int) -> dict:
        """Delete a book by ID."""
        if book_id not in self.books_db:
            raise BookNotFoundException(book_id=book_id)

        deleted_book = self.books_db.pop(book_id)
        return deleted_book

    def update_book(self, book_id: int, title: str = None, author: str = None) -> dict:
        """Update an existing book."""

        if book_id not in self.books_db:
            raise BookNotFoundException(book_id=book_id)

        book = self.books_db[book_id]

        # Validate and update title
        if title is not None:
            if not (3 <= len(title.strip()) <= 100):
                raise InvalidBookDataException(
                    detail="Title validation failed",
                    validation_errors={
                        "title": "Title must be between 3 and 100 characters long"
                    },
                )

            # Check if another book has this title
            for existing_id, existing_book in self.books_db.items():
                if (
                    existing_id != book_id
                    and existing_book["title"].lower() == title.strip().lower()
                ):
                    raise BookAlreadyExistsException(book_title=title)

            book["title"] = title.strip()

        # Validate and update author
        if author is not None:
            if not author or not author.strip():
                raise InvalidBookDataException(
                    detail="Author validation failed",
                    validation_errors={"author": "Author cannot be empty"},
                )
            book["author"] = author.strip()

        return book
