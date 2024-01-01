from fastapi import HTTPException, status


class DeleteIsNotAllowed(HTTPException):
    def __init__(
        self, status_code=status.HTTP_403_FORBIDDEN, detail: str | None = None
    ):
        super().__init__(status_code, detail)


class ParametersError(HTTPException):
    def __init__(
        self, status_code=status.HTTP_400_BAD_REQUEST, detail: str | None = None
    ):
        super().__init__(status_code, detail)


class OutOfStock(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_403_FORBIDDEN,
        detail: str | None = "Out of Stock",
    ):
        super().__init__(status_code, detail)
