# ~/.config/shell_gpt/functions/web_get.py
import urllib.request, urllib.error, urllib.parse
import ssl, sys
from typing import Dict, Optional
from pydantic import Field
from instructor import OpenAISchema

UA = "ShellGPT-Web/1.0 (+https://github.com/TheR1D/shell_gpt)"

class Function(OpenAISchema):
    """
    Fetch a URL with HTTP GET and return status, headers, and a truncated body preview.
    """

    url: str = Field(..., description="HTTP/HTTPS URL to fetch.")
    timeout_sec: int = Field(20, ge=1, le=120, description="Request timeout seconds.")
    max_preview_bytes: int = Field(65536, ge=1024, le=1048576, description="Max body bytes to include in response preview.")
    user_agent: Optional[str] = Field(None, description="Override User-Agent header.")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description="Extra headers.")

    class Config:
        title = "web_get"

    @classmethod
    def execute(cls, url: str, timeout_sec: int = 20, max_preview_bytes: int = 65536,
                user_agent: Optional[str] = None, headers: Optional[Dict[str, str]] = None) -> str:
        headers = headers or {}
        headers.setdefault("User-Agent", user_agent or UA)
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout_sec, context=ctx) as resp:
                status = resp.status
                hdrs = dict(resp.headers.items())
                body = resp.read(max_preview_bytes)
                truncated = resp.length is None or (resp.length > len(body))
                preview = body.decode(hdrs.get("Content-Encoding","utf-8"), errors="replace") \
                          if isinstance(body, (bytes, bytearray)) else str(body)
                note = " (truncated)" if truncated else ""
                return f"Status: {status}\nHeaders: {hdrs}\n\nBody preview{note}:\n{preview}"
        except urllib.error.HTTPError as e:
            return f"HTTPError {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return f"URLError: {e.reason}"
        except Exception as e:
            return f"Error: {e}"
