from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "loja_games"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
