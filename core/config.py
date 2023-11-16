# import secrets
# from typing import Any, Dict, List, Optional, Union
# from pydantic_settings import BaseSettings
# from pydantic import AnyHttpUrl, HttpUrl, PostgresDsn, field_validator


# class Settings(BaseSettings):
#     SECRET_KEY: str = secrets.token_urlsafe(32)
#     # 60 minutes * 24 hours * 8 days = 8 days
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
#     # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
#     # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
#     # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
#     BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

#     @field_validator("BACKEND_CORS_ORIGINS", mode="before")
#     def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
#         if isinstance(v, str) and not v.startswith("["):
#             return [i.strip() for i in v.split(",")]
#         elif isinstance(v, (list, str)):
#             return v
#         raise ValueError(v)

#     PROJECT_NAME: str
#     SENTRY_DSN: Optional[HttpUrl] = None

#     @field_validator("SENTRY_DSN", mode="before")
#     def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
#         if len(v) == 0:
#             return None
#         return v

#     POSTGRES_SERVER: str
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_DB: str
#     SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

#     @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
#     def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
#         if isinstance(v, str):
#             return v
#         return PostgresDsn.build(
#             scheme="postgresql",
#             username=values.get("POSTGRES_USER"),
#             password=values.get("POSTGRES_PASSWORD"),
#             host=values.get("POSTGRES_SERVER"),
#             port=values.get("POSTGRES_PORT"),
#         )

# settings = Settings()
