from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Munesh AI"
    environment: str = "dev"
    redis_url: str = "redis://redis:6379/0"
    postgres_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/munesh"
    llm_model: str = "gpt-5.3-codex"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
