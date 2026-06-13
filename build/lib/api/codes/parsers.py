from __future__ import annotations

import re
from typing import Callable

from bs4 import BeautifulSoup

from api.codes.sources import CodeSource

ParserFunc = Callable[[str], list[str]]


def _find_code_patterns(text: str) -> list[str]:
    found: list[str] = []
    for match in re.finditer(r'\b([A-Z0-9_]{4,})\b', text):
        code = match.group(1)
        if not re.match(r'^[A-Z0-9_]+$', code):
            continue
        if re.match(r'^\d{4,}$', code):
            continue
        found.append(code)
    return found


def _parse_generic(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    codes: list[str] = []
    for tag in soup.find_all(["code", "strong", "b", "td", "th", "li", "p", "span", "h2", "h3"]):
        text = tag.get_text(strip=True)
        codes.extend(_find_code_patterns(text))
    for div in soup.find_all(["article", "div", "section", "main"]):
        text = div.get_text(separator=" ", strip=True)
        codes.extend(_find_code_patterns(text))
    return list(set(codes))


def parse_gamesradar(html: str) -> list[str]:
    return _parse_generic(html)


def parse_gamerant(html: str) -> list[str]:
    return _parse_generic(html)


def parse_game8(html: str) -> list[str]:
    return _parse_generic(html)


def parse_gamewith(html: str) -> list[str]:
    return _parse_generic(html)


def parse_dexerto(html: str) -> list[str]:
    return _parse_generic(html)


_PARSERS: dict[CodeSource, ParserFunc] = {
    CodeSource.GAMESRADAR: parse_gamesradar,
    CodeSource.GAMERANT: parse_gamerant,
    CodeSource.GAME8: parse_game8,
    CodeSource.GAMEWITH: parse_gamewith,
    CodeSource.DEXERTO: parse_dexerto,
}


def get_parser(source: CodeSource) -> ParserFunc | None:
    return _PARSERS.get(source)
