from typing import List

from pydantic import BaseModel as BaseSchema
from pydantic import field_validator

from app.books.models import BookModel


class Author(BaseSchema):
    name: str

    class Config:
        from_attributes = True
    

class Category(BaseSchema):
    name: str

    class Config:
        from_attributes = True

    @field_validator("name")
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
    def from_model(cls, book: BookModel) -> 'Book':
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
