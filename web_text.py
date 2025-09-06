# ~/.config/shell_gpt/functions/web_text.py
import urllib.request, urllib.error, urllib.parse
import ssl, re
from html.parser import HTMLParser
from typing import Optional, Dict
from pydantic import Field
from instructor import OpenAISchema

UA = "ShellGPT-Web/1.0 (+https://github.com/TheR1D/shell_gpt)"

class _TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out = []
        self._skip = False  # inside script/style

    def handle_starttag(self, tag, attrs):
        if tag.lower() in ("script","style"):
            self._skip = True
        elif tag.lower() in ("p","br","div","li","h1","h2","h3","h4","h5","h6"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag.lower() in ("script","style"):
            self._skip = False
        elif tag.lower() in ("p","div","li"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.out.append(data)

    def text(self):
        raw = "".join(self.out)
        raw = re.sub(r"\n\s*\n\s*\n+", "\n\n", raw)
        return raw.strip()

class Function(OpenAISchema):
    """
    Fetch a URL and return a rough plaintext extraction of the HTML.
    """

    url: str = Field(..., description="Page URL.")
    timeout_sec: int = Field(20, ge=1, le=120)
    user_agent: Optional[str] = Field(None)
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)

    class Config:
        title = "web_text"

    @classmethod
    def execute(cls, url: str, timeout_sec: int = 20, user_agent: Optional[str] = None,
                headers: Optional[Dict[str, str]] = None) -> str:
        headers = headers or {}
        headers.setdefault("User-Agent", user_agent or UA)
        ctx = ssl.create_default_context()
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=timeout_sec, context=ctx) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            p = _TextParser()
            p.feed(body)
            return p.text()[:200_000]  # cap output
        except urllib.error.HTTPError as e:
            return f"HTTPError {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return f"URLError: {e.reason}"
        except Exception as e:
            return f"Error: {e}"
