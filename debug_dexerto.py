import httpx, asyncio
from api.codes.parsers import get_parser

async def main():
    parser = get_parser("dexerto")
    async with httpx.AsyncClient(timeout=15) as c:
        resp = await c.get(
            "https://www.dexerto.com/codes/blue-archive-codes-3311458/",
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
        )
        codes = parser(resp.text)
        for c in codes:
            print(f"{c['code']}: {c['rewards'][:60]}")

asyncio.run(main())
