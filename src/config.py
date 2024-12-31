from pydantic import computed_field
from pydantic_settings import BaseSettings


# pylint: disable-next=too-few-public-methods
class Settings(BaseSettings):
    environment: str

    model_path: str
    model_name: str

    storage_provider: str = "s3"
    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    @computed_field
    @property
    def postgres_url(self) -> str:
        # pylint: disable-next=line-too-long
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    # pylint: disable-next=too-few-public-methods
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
