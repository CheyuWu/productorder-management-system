from pydantic import BaseModel


class loginResp(BaseModel):
    access_token: str
    token_type: str
