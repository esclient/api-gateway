from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
    )

    host: str = Field(validation_alias="HOST")
    port: int = Field(validation_alias="PORT")

    comment_service_host: str = Field(validation_alias="COMMENT_SERVICE_HOST")
    comment_service_port: int = Field(validation_alias="COMMENT_SERVICE_PORT")

    rating_service_host: str = Field(validation_alias="RATING_SERVICE_HOST")
    rating_service_port: int = Field(validation_alias="RATING_SERVICE_PORT")

    mod_service_host: str = Field(validation_alias="MOD_SERVICE_HOST")
    mod_service_port: int = Field(validation_alias="MOD_SERVICE_PORT")

    @property
    def comment_service_url(self) -> str:
        return f"{self.comment_service_host}:{self.comment_service_port}"

    @property
    def rating_service_url(self) -> str:
        return f"{self.rating_service_host}:{self.rating_service_port}"

    @property
    def mod_service_url(self) -> str:
        return f"{self.mod_service_host}:{self.mod_service_port}"
