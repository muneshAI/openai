from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'AI Fitness Tracker API'
    environment: str = 'development'
    secret_key: str = 'change-me'
    access_token_expire_minutes: int = 60 * 24
    database_url: str = 'postgresql+psycopg2://postgres:postgres@db:5432/fitness'
    redis_url: str = 'redis://redis:6379/0'
    fcm_credentials_path: str | None = None
    openai_api_key: str | None = None


settings = Settings()
