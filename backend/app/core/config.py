from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Classic Library API"
    APP_ENV: str = "development"

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DATABASE: str = "classic_library"

    FRONTEND_URL: str = "http://localhost:5173"

    model_config = {"env_file": ".env"}


settings = Settings()
