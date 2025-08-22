from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://dell:dell123@localhost:5432/user_db"
    jwt_secret: str = Field(default="change-me-in-prod", alias="JWT_SECRET")
    access_token_expires_min: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRES_MIN")
    
settings = Settings()
