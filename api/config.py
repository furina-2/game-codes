from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 1078
    api_token: str = ""
    wuwa_new_code_webhook: str = ""
    nte_new_code_webhook: str = ""
    bluearchive_new_code_webhook: str = ""
    endfield_new_code_webhook: str = ""


settings = Settings()
