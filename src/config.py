from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "papergraph"
    postgres_password: str = "papergraph"
    postgres_db: str = "papergraph"
    postgres_host: str = "localhost"
    postgres_port: int = 5450
    api_base_url: str = "http://localhost:8030"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
