from pydantic import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str
    ADMIN_USER: str
    ADMIN_PASS: str

    class Config:
        env_file = ".env"

settings = Settings()
