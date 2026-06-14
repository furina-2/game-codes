from __future__ import annotations

import asyncio

import httpx
from loguru import logger

from api.codes.parsers import get_parser
from api.core.registry import get_integration


async def scrape_game_codes(game_slug: str) -> list[dict]:
    integration = get_integration(game_slug)
    if not integration:
        return []

    async def fetch_source(source: str, url: str) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                    follow_redirects=True,
                )
                if resp.status_code != 200:
                    logger.warning(f"{source} returned {resp.status_code} for {game_slug}")
                    return []
                parser = get_parser(source)
                if not parser:
                    return []
                parsed = parser(resp.text)
                logger.info(f"Scraped {len(parsed)} codes from {source} for {game_slug}")
                return parsed
        except asyncio.TimeoutError:
            logger.warning(f"Timeout scraping {source} for {game_slug}")
            return []
        except Exception as e:
            logger.error(f"Failed scraping {source} for {game_slug}: {e}")
            return []

    tasks = [
        fetch_source(source, url)
        for source, url in integration.code_urls.items()
    ]
    results = await asyncio.gather(*tasks)

    seen: dict[str, dict] = {}
    for entries in results:
        for entry in entries:
            code = entry["code"].upper()
            if code not in seen:
                seen[code] = {"rewards": entry.get("rewards", ""), "expires_at": entry.get("expires_at", "")}
            else:
                if entry.get("rewards") and not seen[code]["rewards"]:
                    seen[code]["rewards"] = entry["rewards"]
                if entry.get("expires_at") and not seen[code]["expires_at"]:
                    seen[code]["expires_at"] = entry["expires_at"]

    return [{"code": c, "game": game_slug, **v} for c, v in seen.items()]
