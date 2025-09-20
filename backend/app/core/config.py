from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
	app_name: str = "Sweet Shop API"
	secret_key: str = Field(default="dev-secret-change", alias="SECRET_KEY")
	access_token_expires_minutes: int = Field(default=60 * 24, alias="ACCESS_TOKEN_EXPIRES_MINUTES")
	mongo_uri: str = Field(default="mongodb://root:example@localhost:27017/?authSource=admin", alias="MONGO_URI")
	database_name: str = Field(default="sweetshop", alias="MONGO_DB")
	allowed_origins_csv: str = Field(default="http://localhost:5173,http://127.0.0.1:5173", alias="ALLOWED_ORIGINS")

	class Config:
		env_file = "backend/.env"
		env_file_encoding = "utf-8"


settings = Settings()
