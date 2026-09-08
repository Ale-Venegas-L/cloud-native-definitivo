from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Classic Library API"
    APP_ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DATABASE: str = "classic_library"

    FRONTEND_URL: str = "http://localhost:5173"

    COGNITO_REGION: str = "us-east-1"
    COGNITO_USER_POOL_ID: str = ""
    COGNITO_APP_CLIENT_ID: str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
