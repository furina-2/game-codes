from __future__ import annotations

from pydantic import BaseModel, field_validator

from api.constants import Game


class CreateCode(BaseModel):
    code: str
    game: str

    @field_validator("code")
    @classmethod
    def __upper_code(cls, v: str) -> str:
        return v.upper()

    @field_validator("game")
    @classmethod
    def __valid_game(cls, v: str) -> str:
        if v not in Game.values():
            raise ValueError(f"Invalid game: {v}. Must be one of {Game.values()}")
        return v
