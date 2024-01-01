from fastapi import HTTPException, status


class NotAuthCurrentUser(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    ) -> None:
        super().__init__(status_code, detail, headers)
