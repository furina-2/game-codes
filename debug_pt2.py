import httpx, asyncio
from bs4 import BeautifulSoup
from api.codes.parsers import get_parser, _container, SELECTORS, CodeSource

async def main():
    async with httpx.AsyncClient(timeout=15) as c:
        resp = await c.get(
            "https://www.pockettactics.com/blue-archive/codes",
            headers={"User-Agent": "Mozilla/5.0"},
            follow_redirects=True,
        )
        print(f"Status: {resp.status_code}, Size: {len(resp.text)}")
        
        soup = BeautifulSoup(resp.text, "lxml")
        el = soup.select_one(".entry-content")
        print(f".entry-content found: {el is not None}")
        if el:
            lis = el.find_all("li")
            print(f"  li count: {len(lis)}")
        
        parser = get_parser("pockettactics")
        codes = parser(resp.text)
        print(f"Parser returned: {len(codes)} codes")
        for c in codes:
            print(f"  {c['code']}")

asyncio.run(main())
