from app.exceptions import NotFound


class ErrorCode:
    BOOK_NOT_FOUND = "Book(s) not found."


class BookNotFound(NotFound):
    DETAIL = ErrorCode.BOOK_NOT_FOUND
