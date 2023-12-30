from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: Optional[bool] = False
    database_url: Optional[str] = None
    model_config = SettingsConfigDict(env_file="app.env")
