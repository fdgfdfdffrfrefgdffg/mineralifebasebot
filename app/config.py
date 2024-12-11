from pydantic_settings import BaseSettings

class Config(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str = "sqlite:///water_delivery.db"  # SQLite uchun

    class Config:
        env_file = ".env"

config = Config()
