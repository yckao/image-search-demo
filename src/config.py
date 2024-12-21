from pydantic import computed_field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_dir: str = "models/clip-vit-base-patch32"
    model_name: str = "openai/clip-vit-base-patch32"

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
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
