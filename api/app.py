from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles

from api.config import settings
from api.constants import CodeStatus, Game, GAME_DESCRIPTIONS, GAME_NAMES
from api.codes.task import check_codes, update_codes
from api.db import db
from api.discord_bot import CodeBot
from api.models import CreateCode, UpdateCode
from api.ratelimit import RateLimitMiddleware

security = HTTPBearer(auto_error=False)


def verify_token(credentials: HTTPAuthorizationCredentials | None = Security(security)):
    if not settings.api_token:
        return True
    if not credentials or credentials.credentials != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True


bot = CodeBot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    discord_task = None
    if settings.discord_token:
        await bot.login(settings.discord_token)
        discord_task = asyncio.create_task(bot.connect())
        await bot.wait_until_ready()
    yield
    if discord_task:
        discord_task.cancel()
        await bot.close()


app = FastAPI(title="Game Codes API", lifespan=lifespan)
app.add_middleware(RateLimitMiddleware, max_requests=30, window=60)
app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.get("/", response_class=FileResponse)
async def index():
    return FileResponse("api/static/index.html")


@app.get("/api-docs", response_class=FileResponse)
async def api_docs():
    return FileResponse("api/static/api-docs.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/stats")
async def stats():
    result = {}
    for slug in Game.values():
        codes = await db.redeemcode.find_many(
            where={"game": slug, "status": CodeStatus.OK},
        )
        unverified = await db.redeemcode.find_many(
            where={"game": slug, "status": CodeStatus.UNVERIFIED},
        )
        result[slug] = {"codes": len(codes), "unverified": len(unverified)}
    return result


@app.get("/games")
async def list_games():
    return {
        slug: {"name": GAME_NAMES.get(slug, ""), "description": GAME_DESCRIPTIONS.get(slug, "")}
        for slug in Game.values()
    }


@app.get("/codes")
async def get_codes(game: str):
    if game not in Game.values():
        raise HTTPException(
            status_code=404,
            detail=f"Unknown game: {game}. Must be one of {Game.values()}",
        )
    codes = await db.redeemcode.find_many(
        where={"game": game, "status": CodeStatus.OK},
        order={"id": "desc"},
    )
    unverified = await db.redeemcode.find_many(
        where={"game": game, "status": CodeStatus.UNVERIFIED},
        order={"id": "desc"},
    )
    return {
        "game": game,
        "codes": [
            {"id": c.id, "code": c.code, "rewards": c.rewards, "source": c.source}
            for c in codes
        ],
        "unverified": [
            {"id": c.id, "code": c.code, "rewards": c.rewards, "source": c.source}
            for c in unverified
        ],
    }


@app.post("/codes")
async def add_code(data: CreateCode, _=Depends(verify_token)):
    existing = await db.redeemcode.find_first(
        where={"code": data.code, "game": data.game}
    )
    if existing:
        raise HTTPException(status_code=409, detail="Code already exists")
    created = await db.redeemcode.create(data={
        "code": data.code,
        "game": data.game,
        "status": CodeStatus.UNVERIFIED,
        "rewards": "",
        "source": "manual",
    })
    return {"id": created.id, "code": created.code}


@app.patch("/codes/{code_id}")
async def update_code_status(code_id: int, data: UpdateCode, _=Depends(verify_token)):
    existing = await db.redeemcode.find_unique(where={"id": code_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Code not found")
    await db.redeemcode.update(
        where={"id": code_id},
        data={"status": data.status},
    )
    return {"ok": True, "code": existing.code, "status": data.status}


@app.delete("/codes/{code_id}")
async def delete_code(code_id: int, _=Depends(verify_token)):
    await db.redeemcode.delete(where={"id": code_id})
    return {"ok": True}


@app.post("/update-codes")
async def trigger_update(_=Depends(verify_token)):
    await update_codes()
    return {"ok": True}


@app.post("/check-codes")
async def trigger_check(_=Depends(verify_token)):
    await check_codes()
    return {"ok": True}
