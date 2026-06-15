import httpx, asyncio
from bs4 import BeautifulSoup
from api.codes.parsers import get_parser

async def main():
    url = "https://www.pockettactics.com/blue-archive/codes"
    async with httpx.AsyncClient(timeout=15) as c:
        resp = await c.get(url, headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True)
        soup = BeautifulSoup(resp.text, "lxml")
        
        # Find RABBITHOLE
        for code in ["RABBITHOLE", "RUNEREADER"]:
            strong = soup.find("strong", string=lambda t: t and code in t.strip().upper())
            if strong:
                prev_h = strong.find_previous(["h1","h2","h3","h4","h5","h6","a"])
                if prev_h:
                    print(f"{code}: prev heading <{prev_h.name}> text='{prev_h.get_text(strip=True)}'")
                else:
                    print(f"{code}: no previous heading")
        
        # Also let the parser run to see all codes
        parser = get_parser("pockettactics")
        codes = parser(resp.text)
        print(f"\nPocketTactics parser returns:")
        for c in codes:
            print(f"  {c['code']}: {c.get('rewards','')[:60]}")
        
asyncio.run(main())
