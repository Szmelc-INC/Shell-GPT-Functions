# ~/.config/shell_gpt/functions/web_extract_links.py
import urllib.request, urllib.error, urllib.parse
import ssl
from html.parser import HTMLParser
from typing import List, Tuple, Optional, Dict
from pydantic import Field
from instructor import OpenAISchema

UA = "ShellGPT-Web/1.0 (+https://github.com/TheR1D/shell_gpt)"

class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: List[Tuple[str, str]] = []  # (href, text)
        self._in_a = False
        self._buf = ""
        self._curr_href = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self._in_a = True
            self._buf = ""
            self._curr_href = dict(attrs).get("href")

    def handle_data(self, data):
        if self._in_a:
            self._buf += data

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._in_a:
            text = " ".join(self._buf.split())
            href = self._curr_href or ""
            self.links.append((href, text))
            self._in_a = False
            self._buf = ""
            self._curr_href = None

class Function(OpenAISchema):
    """
    Download a page and extract all anchor links (href + text).
    """

    url: str = Field(..., description="Page URL.")
    timeout_sec: int = Field(20, ge=1, le=120)
    user_agent: Optional[str] = Field(None)
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)

    class Config:
        title = "web_extract_links"

    @classmethod
    def execute(cls, url: str, timeout_sec: int = 20, user_agent: Optional[str] = None,
                headers: Optional[Dict[str, str]] = None) -> str:
        headers = headers or {}
        headers.setdefault("User-Agent", user_agent or UA)
        ctx = ssl.create_default_context()
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=timeout_sec, context=ctx) as resp:
                content_type = resp.headers.get("Content-Type","")
                body = resp.read().decode("utf-8", errors="replace")
            if "html" not in content_type.lower() and "<html" not in body.lower():
                return "Not HTML content; no links extracted."
            p = _LinkParser()
            p.feed(body)
            if not p.links:
                return "No links found."
            lines = [f"- {href}  —  {text}" for href, text in p.links if href]
            return "\n".join(lines[:500])
        except urllib.error.HTTPError as e:
            return f"HTTPError {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return f"URLError: {e.reason}"
        except Exception as e:
            return f"Error: {e}"
