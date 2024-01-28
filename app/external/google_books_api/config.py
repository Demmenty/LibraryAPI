from pydantic_settings import BaseSettings


class GoogleBooksConfig(BaseSettings):
    GOOGLE_BOOKS_API: str = "https://www.googleapis.com/books/v1"


gb_config = GoogleBooksConfig()
