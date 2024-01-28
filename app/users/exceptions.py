from app.exceptions import BadRequest


class ErrorCode:
    EMAIL_TAKEN = "Email is already taken."
    USERNAME_TAKEN = "Username is already taken."


class EmailTaken(BadRequest):
    DETAIL = ErrorCode.EMAIL_TAKEN


class UsernameTaken(BadRequest):
    DETAIL = ErrorCode.USERNAME_TAKEN
