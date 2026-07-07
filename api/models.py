from __future__ import annotations

from pydantic import BaseModel, field_validator

from api.constants import Game


class CreateCode(BaseModel):
    code: str
    game: str

    @field_validator("code")
    @classmethod
    def __upper_code(cls, v: str) -> str:
        v = v.upper()
        if len(v) > 50:
            raise ValueError("Code too long (max 50 characters)")
        return v

    @field_validator("game")
    @classmethod
    def __valid_game(cls, v: str) -> str:
        if v not in Game.values():
            raise ValueError(f"Invalid game: {v}. Must be one of {Game.values()}")
        return v


class UpdateCode(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def __valid_status(cls, v: str) -> str:
        v = v.upper()
        if v not in ("OK", "NOT_OK", "UNVERIFIED"):
            raise ValueError("Status must be OK, NOT_OK, or UNVERIFIED")
        return v


class VerifyCodes(BaseModel):
    game: str
    codes: list[str]

    @field_validator("game")
    @classmethod
    def __valid_game(cls, v: str) -> str:
        if v not in Game.values():
            raise ValueError(f"Invalid game: {v}. Must be one of {Game.values()}")
        return v
