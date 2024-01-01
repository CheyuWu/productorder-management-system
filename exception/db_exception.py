from fastapi import HTTPException, status


class DatabaseUrlNotFound(BaseException):
    pass


class UserExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        message: str | None = "User Exists",
    ) -> None:
        super().__init__(status_code, message)


class UserNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        message: str | None = "User not found",
    ) -> None:
        super().__init__(status_code, message)


class ProductNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        message: str | None = "Product not found",
    ) -> None:
        super().__init__(status_code, message)
