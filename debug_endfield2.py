import httpx, asyncio
from bs4 import BeautifulSoup
from api.codes.parsers import get_parser, _find_li_content

async def main():
    async with httpx.AsyncClient(timeout=15) as c:
        resp = await c.get(
            "https://www.gamesradar.com/games/rpg/arknights-endfield-codes/",
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
        )
        soup = BeautifulSoup(resp.text, "lxml")
        
        for sel in [".article-body", ".content", "article"]:
            el = soup.select_one(sel)
            if el:
                lis = el.find_all("li")
                strongs = el.find_all("strong")
                print(f"{sel}: found, {len(lis)} li, {len(strongs)} strong")
            else:
                print(f"{sel}: not found")
        
        # Try parser directly
        parser = get_parser("gamesradar")
        codes = parser(resp.text)
        print(f"\nParser returned: {[c['code'] for c in codes]}")

asyncio.run(main())
