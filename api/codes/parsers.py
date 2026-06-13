from __future__ import annotations

import re
from typing import Callable

from bs4 import BeautifulSoup

from api.codes.sources import CodeSource

ParserFunc = Callable[[str], list[str]]

NOISE_WORDS: set[str] = {
    "ABOUT", "ACCESS", "ACCOUNT", "ARCHIVE", "ARTICLES", "ARTICLESTAGS",
    "BACK", "CATEGORIES", "COMMUNITY", "CONTACT", "CONTENT", "COOKIE",
    "COPYRIGHT", "DETAILS", "EMAIL", "ERROR", "EVENT", "FAQ", "FIND",
    "FOOTER", "GUIDE", "HEADER", "HELP", "HOME", "IMAGE", "INDEX",
    "INTERVIEW", "JOIN", "LANGUAGE", "LATEST", "LEARN", "LINK", "LINKS",
    "LOAD", "LOGIN", "LOGOUT", "MAGAZINE", "MAIL", "MEDIA", "MENU",
    "META", "MOBILE", "MORE", "NAV", "NAVIGATION", "NEWS", "NEXT",
    "NONE", "NOTE", "NOTES", "OFF", "ON", "OPEN", "OTHER", "PAGE",
    "PAGES", "PHOTO", "POPULAR", "POST", "POSTS", "PREV", "PREVIOUS",
    "PRICE", "PRIVACY", "PROFILE", "PUBLIC", "QUICK", "RANDOM",
    "READ", "RECENT", "REGISTER", "RELATED", "REPLY", "REPORT",
    "SAVE", "SCREEN", "SEARCH", "SECURITY", "SHARE", "SHOP", "SIGN",
    "SITEMAP", "SKIP", "SOCIAL", "STORY", "SUBMIT", "SUPPORT",
    "TAGS", "TERMS", "TITLE", "TOP", "TOPICS", "TUTORIAL", "TWITTER",
    "UPDATE", "UPLOAD", "URL", "USER", "VIDEO", "VIEW", "WEB",
    "WEBSITE", "WELCOME", "WIDGET", "WIKI", "WRITE", "YOUTUBE",
    "CODE", "CODES", "REWARDS", "REDEEM", "EXPIRED", "ACTIVE",
    "GIFT", "FREE", "BONUS", "REWARD", "PROMO", "COUPON",
    "LOAD", "MORE", "LESS", "SHOW", "HIDE",
    "COPY", "SHARE", "TWEET", "FACEBOOK", "REDDIT", "DISCORD",
    "GAMING", "POPULAR", "VIEW", "ALL", "GAMES", "TRENDING",
    "NEW", "PC", "PS5", "XBOX", "NINTENDO", "MOBILE", "ANDROID", "IOS",
    "LOG", "SIGN", "IN", "UP", "OUT", "MY", "YOUR", "OUR", "THEIR",
    "THIS", "THAT", "WITH", "FROM", "HAVE", "BEEN", "BEING",
    "FIRST", "LAST", "NEXT", "PREV", "MENU", "NAV",
    "CLICK", "ENTER", "TYPE", "INPUT", "FIELD", "FORM", "BUTTON",
    "CANCEL", "CLOSE", "DONE", "EDIT", "DELETE", "REMOVE", "ADD",
    "CREATE", "UPDATE", "MANAGE", "SETTINGS", "OPTIONS", "CONFIG",
    "ACCOUNT", "PROFILE", "PASSWORD", "EMAIL", "PHONE", "NUMBER",
    "ADDRESS", "CITY", "STATE", "COUNTRY", "ZIP", "CODE",
    "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY",
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY",
    "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER",
    "SPRING", "SUMMER", "AUTUMN", "WINTER",
    "ANNIVERSARY", "BIRTHDAY", "CELEBRATION", "FESTIVAL", "EVENT",
    "DAILY", "WEEKLY", "MONTHLY", "YEARLY", "SPECIAL", "LIMITED",
    "GUEST", "MEMBER", "PREMIUM", "BASIC", "STANDARD", "PRO",
    "ADMIN", "MOD", "OWNER", "CREATOR", "EDITOR", "AUTHOR",
    "STARS", "RATING", "SCORE", "LEVEL", "RANK", "TIER",
    "POLL", "SURVEY", "VOTE", "RESULT",
    "ANSWER", "QUESTION", "SOLUTION", "TIP", "TRICK", "GUIDE",
    "INFO", "INFORMATION", "DATA", "TABLE", "LIST", "ITEM",
    "CHECK", "VERIFY", "CONFIRM", "SUCCESS", "FAIL", "ERROR",
    "WARNING", "NOTICE", "ALERT", "MESSAGE", "NOTIFICATION",
    "STREAM", "LIVE", "VIDEO", "AUDIO", "MEDIA", "IMAGE", "PHOTO",
    "GALLERY", "ALBUM", "COLLECTION", "SET",
    "SOURCE", "SITES", "SITE", "PAGE", "DOC", "DOCS", "DOCUMENT",
    "FILE", "FILES", "FOLDER", "DIRECTORY", "PATH",
    "SERVER", "CLIENT", "HOST", "LOCAL", "REMOTE", "GLOBAL",
    "ENGLISH", "SPANISH", "FRENCH", "GERMAN", "JAPANESE", "KOREAN",
    "CHINESE", "RUSSIAN", "ARABIC", "HINDI",
    "PSM3", "PTCGP", "BDSP", "ST79", "C2000", "B100", "M1000",
    "INFERNO", "MANISH", "FIND",
}

NOISE_PREFIXES: tuple[str, ...] = (
    "BTN_", "LBL_", "TXT_", "MSG_", "ERR_", "WARN_",
    "NAV_", "MENU_", "FOOTER_", "HEADER_",
    "PLACEHOLDER_", "DEFAULT_",
)


def _is_noise(code: str) -> bool:
    if code in NOISE_WORDS:
        return True
    if code.startswith(NOISE_PREFIXES):
        return True
    if re.match(r'^[A-Z][a-z]{2,}$', code):
        return True
    if re.match(r'^[A-Z]{2,3}\d{2,}$', code):
        return True
    if re.match(r'^\d{5,}', code):
        return True
    half = len(code) // 2
    if len(code) >= 8 and len(code) % 2 == 0 and code[:half] == code[half:]:
        return True
    return False


def _find_code_patterns(text: str) -> list[str]:
    found: list[str] = []
    for match in re.finditer(r'\b([A-Z0-9_]{4,})\b', text):
        code = match.group(1)
        if not re.match(r'^[A-Z0-9_]+$', code):
            continue
        if re.match(r'^\d{4,}$', code):
            continue
        if _is_noise(code):
            continue
        found.append(code)
    return found


def _parse_tables(soup: BeautifulSoup) -> list[str]:
    codes: list[str] = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["td", "th"])
            for cell in cells:
                text = cell.get_text(strip=True)
                for code in _find_code_patterns(text):
                    codes.append(code)
    return codes


def _parse_structured_elements(soup: BeautifulSoup) -> list[str]:
    codes: list[str] = []
    for tag in soup.find_all(["code", "strong", "b", "td", "th", "li"]):
        text = tag.get_text(strip=True)
        if len(text) < 100:
            codes.extend(_find_code_patterns(text))
    return codes


def _parse_full_text(soup: BeautifulSoup) -> list[str]:
    codes: list[str] = []
    for div in soup.find_all(["article", "div", "section", "main"]):
        text = div.get_text(separator=" ", strip=True)
        codes.extend(_find_code_patterns(text))
    return codes


def _parse_generic(html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    codes: list[str] = []
    codes.extend(_parse_tables(soup))
    codes.extend(_parse_structured_elements(soup))
    codes.extend(_parse_full_text(soup))
    seen: set[str] = set()
    unique: list[str] = []
    for c in codes:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


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


def parse_pcgamesn(html: str) -> list[str]:
    return _parse_generic(html)


def parse_vg247(html: str) -> list[str]:
    return _parse_generic(html)


def parse_wutheringgg(html: str) -> list[str]:
    return _parse_generic(html)


def parse_eurogamer(html: str) -> list[str]:
    return _parse_generic(html)


def parse_pockettactics(html: str) -> list[str]:
    return _parse_generic(html)


_PARSERS: dict[CodeSource, ParserFunc] = {
    CodeSource.GAMESRADAR: parse_gamesradar,
    CodeSource.GAMERANT: parse_gamerant,
    CodeSource.GAME8: parse_game8,
    CodeSource.GAMEWITH: parse_gamewith,
    CodeSource.DEXERTO: parse_dexerto,
    CodeSource.PCGAMESN: parse_pcgamesn,
    CodeSource.VG247: parse_vg247,
    CodeSource.WUTHERINGGG: parse_wutheringgg,
    CodeSource.EUROGAMER: parse_eurogamer,
    CodeSource.POCKETTACTICS: parse_pockettactics,
}


def get_parser(source: CodeSource) -> ParserFunc | None:
    return _PARSERS.get(source)
