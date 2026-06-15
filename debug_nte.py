import asyncio
import httpx
from api.codes.sources import CODE_URLS, Game, CodeSource
from api.codes.parsers import get_parser

async def main():
    for src_name, url in CODE_URLS[Game.nte].items():
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                    follow_redirects=True,
                )
                if resp.status_code == 200:
                    parser = get_parser(src_name.value)
                    if parser:
                        codes = parser(resp.text)
                        print(f"{src_name.value}: {[c['code'] for c in codes]}")
        except Exception as e:
            print(f"{src_name.value}: error - {e}")

asyncio.run(main())
