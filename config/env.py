from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class EnvironmentVariables(BaseSettings):
    DJANGO_DB_NAME: str
    DJANGO_DB_USER: str
    DJANGO_DB_PASSWORD: str
    DJANGO_DB_HOST: str
    DJANGO_DB_PORT: int = 5432
    DJANGO_SECRET_KEY: str
    DJANGO_DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


env = EnvironmentVariables.model_validate({})
