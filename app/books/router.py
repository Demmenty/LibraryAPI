import json

from fastapi import APIRouter, BackgroundTasks, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependiencies import get_user_from_access_token
from app.books import schemas
from app.books.dependiencies import validate_isbn_10
from app.books.exceptions import BookNotFound
from app.books.service import BookService
from app.database import get_db
from app.external.google_books_api.service import GoogleBooksService
from app.external.redis_db.schemas import RedisData
from app.external.redis_db.service import redis_service
from app.users.models import UserModel

router = APIRouter()


@router.get("/isbn/{isbn}", response_model=schemas.Book)
async def get_book_by_isbn(
    worker: BackgroundTasks,
    isbn: str = Depends(validate_isbn_10),
    db: AsyncSession = Depends(get_db),
    book_service: BookService = Depends(BookService),
    google_books_api: GoogleBooksService = Depends(GoogleBooksService),
    user: UserModel = Depends(get_user_from_access_token),
) -> dict:
    """Retrieves a book details by ISBN"""

    cached_book = await redis_service.get_by_key(f"book:{isbn}")
    if cached_book:
        book_schema = schemas.Book(**json.loads(cached_book))
        return book_schema

    book_db = await book_service.get_book_by_isbn(db, isbn)
    if book_db:
        book_schema = schemas.Book.from_model(book_db)
    else:
        book_schema = await google_books_api.get_book_by_isbn(isbn)
        if not book_schema:
            raise BookNotFound()

        worker.add_task(book_service.create_book, db, book_schema)

    cache_data = RedisData(
        key=f"book:{isbn}", value=book_schema.model_dump_json(), ttl=3600
    )
    worker.add_task(redis_service.set_key, cache_data)

    return book_schema


@router.get("/category/{category}", response_model=schemas.BookList)
async def get_books_by_category(
    worker: BackgroundTasks,
    category: str = Path(..., title="Category in URL"),
    db: AsyncSession = Depends(get_db),
    book_service: BookService = Depends(BookService),
    user: UserModel = Depends(get_user_from_access_token),
) -> dict:
    """Retrieves books details by category"""

    cached_books = await redis_service.get_by_key(f"book:{category}")
    if cached_books:
        books_schema = schemas.BookList(
            books=[schemas.Book(**json.loads(book)) for book in json.loads(cached_books)]
        )
        return books_schema

    books_db = await book_service.get_books_by_category(db, category)
    if not books_db:
        raise BookNotFound()

    books_schema = schemas.BookList(
        books=[schemas.Book.from_model(book) for book in books_db]
    )

    cache_data = RedisData(
        key=f"book:{category}",
        value=json.dumps([book.model_dump_json() for book in books_schema.books]),
        ttl=1200,
    )
    worker.add_task(redis_service.set_key, cache_data)

    return books_schema


@router.post("/search", response_model=schemas.BookList)
async def search_books(
    worker: BackgroundTasks,
    search_query: schemas.BookSearchQuery,
    db: AsyncSession = Depends(get_db),
    book_service: BookService = Depends(BookService),
    user: UserModel = Depends(get_user_from_access_token),
) -> dict:
    """Retrieves books details based on the search query"""

    cached_books = await redis_service.get_by_key(f"book:{search_query}")
    if cached_books:
        books_schema = schemas.BookList(
            books=[schemas.Book(**json.loads(book)) for book in json.loads(cached_books)]
        )
        return books_schema

    books_db = await book_service.search_books(db, search_query)
    if not books_db:
        raise BookNotFound()

    books_schema = schemas.BookList(
        books=[schemas.Book.from_model(book) for book in books_db]
    )

    cache_data = RedisData(
        key=f"book:{search_query}",
        value=json.dumps([book.model_dump_json() for book in books_schema.books]),
        ttl=1200,
    )
    worker.add_task(redis_service.set_key, cache_data)

    return books_schema


# TODO remove
@router.get("/all", response_model=schemas.BookList)
async def get_all_books(
    db: AsyncSession = Depends(get_db),
    book_service: BookService = Depends(BookService),
    user: UserModel = Depends(get_user_from_access_token),
) -> dict:
    books_db = await book_service.get_all_books(db)
    if not books_db:
        raise BookNotFound()

    books_schema = schemas.BookList(
        books=[schemas.Book.from_model(book) for book in books_db]
    )
    return books_schema
