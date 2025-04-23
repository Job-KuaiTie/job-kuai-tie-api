from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    secret_key: str = Field(alias="SECRET_KEY")
    database_url: Optional[str] = Field(default=None, alias="DB_URL")
    algorithm: Optional[str] = Field(default="HS256", alias="ALGORITHM")

    db_type: str = Field(default="sqlite", alias="DB_TYPE")
    db_user: Optional[str] = Field(default=None, alias="DB_USER")
    db_password: Optional[str] = Field(default=None, alias="DB_PASSWORD")
    db_host: Optional[str] = Field(default=None, alias="DB_HOST")
    db_port: Optional[int] = Field(default=None, alias="DB_PORT")
    db_name: Optional[str] = Field(default=None, alias="DB_NAME")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Define the database url here
    @property
    def db_url(self):
        # If provide database variables
        if self.db_user and self.db_password and self.db_host and self.db_name:
            port_part = f":{self.db_port}" if self.db_port else ""

            if self.db_type == "mysql":
                return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}{port_part}/{self.db_name}"

            if self.db_type == "postgresql":
                return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}{port_part}/{self.db_name}"
        # If directly provide db_url
        elif self.database_url:
            return self.database_url
        # Database url is required
        else:
            raise ValueError("No valid database config found!")

    # Use relative url to located the .env at root
    model_config = SettingsConfigDict(env_file=f"{Path(__file__).parent.parent}/.env")


settings = Settings()
