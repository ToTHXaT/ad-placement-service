import os

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Config(BaseModel):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_dbname: str
    db_echo: bool

    refresh_token_cookie_name: str
    refresh_token_duration_days: int

    access_token_cookie_name: str
    access_token_duration_minutes: int

    jwt_secret: str
    jwt_algorithm: str


config = Config(
    db_host=os.getenv("DB_HOST"),
    db_port=int(os.getenv("DB_PORT")),
    db_user=os.getenv("DB_USER"),
    db_password=os.getenv("DB_PASSWORD"),
    db_dbname=os.getenv("DB_NAME"),
    db_echo=os.getenv("DB_ECHO").lower() in ("true", "yes", "on"),
    refresh_token_cookie_name=os.getenv("REFRESH_TOKEN_COOKIE_NAME", "refresh_token"),
    refresh_token_duration_days=int(os.getenv("REFRESH_TOKEN_DURATION_DAYS", "30")),
    access_token_cookie_name=os.getenv("ACCESS_TOKEN_COOKIE_NAME", "access_token"),
    access_token_duration_minutes=int(os.getenv("ACCESS_TOKEN_DURATION_MINUTES", "30")),
    jwt_secret=os.getenv("JWT_SECRET", None),
    jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
)

print("Loaded config: ", config)
