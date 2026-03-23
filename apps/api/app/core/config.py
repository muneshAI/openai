from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Munesh AI API"
    environment: str = "development"
    openai_model: str = "gpt-4.1"
    vector_index_name: str = "munesh-memory"
    postgres_dsn: str = "postgresql://munesh:munesh@localhost:5432/munesh"
    redis_url: str = "redis://localhost:6379/0"
    enable_voice: bool = True
    enable_human_approval: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
