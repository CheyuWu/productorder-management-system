from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG: Optional[bool] = False
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = "ae1a95e847d60bdaf40bbbec884167aeffa686a532d15b2e5eb281c5b1db2337"
    ENCRYPT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Import envfile
    model_config = SettingsConfigDict(env_file="app.env")
