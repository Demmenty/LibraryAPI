from pydantic_settings import BaseSettings


class GoogleBooksConfig(BaseSettings):
    GB_API_URL: str = "https://www.googleapis.com/"


gb_config = GoogleBooksConfig()
