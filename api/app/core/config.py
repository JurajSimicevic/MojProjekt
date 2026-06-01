from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str = (
        "postgresql+asyncpg://fd_user:fd_pass@localhost:5432/food_delivery"
    )
    JWT_SECRET: str = "change-me-in-production"
    JWT_ISSUER: str = "food-delivery-api"
    CORS_ORIGINS: str = ""

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def force_asyncpg_scheme(cls, v: str) -> str:
        """Rewrite bare postgresql:// or postgres:// URLs to use the asyncpg
        driver.  Railway injects DATABASE_URL without a driver qualifier, which
        would cause SQLAlchemy to fall back to psycopg2 (not installed)."""
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v

    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS.strip():
            return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]
        return ["http://127.0.0.1:5173", "http://localhost:5173"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
