from app.exceptions import BadRequest, NotFound


class ErrorCode:
    BOOK_NOT_FOUND = "Book(s) not found."
    CATEGORY_NOT_FOUND = "Category(s) not found."
    SEARCH_QUERY_EMPTY = "Search query cannot be empty."


class BookNotFound(NotFound):
    DETAIL = ErrorCode.BOOK_NOT_FOUND


class CategoryNotFound(NotFound):
    DETAIL = ErrorCode.CATEGORY_NOT_FOUND


class SearchQueryEmpty(BadRequest):
    DETAIL = ErrorCode.SEARCH_QUERY_EMPTY
