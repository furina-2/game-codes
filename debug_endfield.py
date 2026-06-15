import httpx, asyncio
from api.codes.parsers import get_parser

async def main():
    urls = [
        ("gamesradar", "https://www.gamesradar.com/games/rpg/arknights-endfield-codes/"),
        ("game8", "https://game8.co/games/Arknights-Endfield/archives/571509"),
    ]
    for name, url in urls:
        async with httpx.AsyncClient(timeout=15) as c:
            resp = await c.get(url, headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True)
            if resp.status_code == 200:
                parser = get_parser(name)
                if parser:
                    codes = parser(resp.text)
                    print(f"{name}: {[c['code'] for c in codes]}")
                else:
                    print(f"{name}: no parser")
            else:
                print(f"{name}: HTTP {resp.status_code}")

asyncio.run(main())
