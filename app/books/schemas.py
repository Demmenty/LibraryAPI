from typing import List

from pydantic import BaseModel as BaseSchema, field_validator, model_validator

from app.books.exceptions import SearchQueryEmpty
from app.books.models import BookModel


class Author(BaseSchema):
    name: str

    class Config:
        from_attributes = True


class Category(BaseSchema):
    name: str

    class Config:
        from_attributes = True

    @field_validator("name", mode="before")
    @classmethod
    def convert_to_lower(cls, value):
        return value.lower()


class Book(BaseSchema):
    isbn: str
    title: str
    language: str
    publication_date: str
    authors: List[Author] = []
    categories: List[Category] = []

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, book: BookModel) -> "Book":
        authors = [Author(name=author.name) for author in book.authors]
        categories = [Category(name=category.name) for category in book.categories]

        book = cls(
            isbn=book.isbn,
            language=book.language,
            title=book.title,
            authors=authors,
            publication_date=book.publication_date,
            categories=categories,
        )
        return book


class BookList(BaseSchema):
    books: List[Book]

    class Config:
        from_attributes = True


class BookSearchQuery(BaseSchema):
    title: str | None = None
    author: str | None = None
    publication_date: str | None = None
    isbn: str | None = None

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def at_least_one_field_not_none(cls, values):
        if all((not field[1] for field in values)):
            raise SearchQueryEmpty()

        return values
