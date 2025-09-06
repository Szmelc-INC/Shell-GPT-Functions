# ~/.config/shell_gpt/functions/web_download.py
import urllib.request, urllib.error, urllib.parse
import ssl, os, hashlib
from typing import Optional, Dict
from pydantic import Field
from instructor import OpenAISchema

UA = "ShellGPT-Web/1.0 (+https://github.com/TheR1D/shell_gpt)"

class Function(OpenAISchema):
    """
    Download a URL to a file path with a size cap and return file info (path, size, sha256).
    """

    url: str = Field(..., description="HTTP/HTTPS URL to download.")
    out_path: str = Field(..., description="Destination file path (will be overwritten).")
    max_bytes: int = Field(50 * 1024 * 1024, ge=1024, le=1024*1024*1024, description="Abort if content exceeds this many bytes.")
    timeout_sec: int = Field(60, ge=1, le=300, description="Request timeout seconds.")
    user_agent: Optional[str] = Field(None, description="Override User-Agent.")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description="Extra headers.")

    class Config:
        title = "web_download"

    @classmethod
    def execute(cls, url: str, out_path: str, max_bytes: int = 50*1024*1024,
                timeout_sec: int = 60, user_agent: Optional[str] = None,
                headers: Optional[Dict[str, str]] = None) -> str:
        headers = headers or {}
        headers.setdefault("User-Agent", user_agent or UA)
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers=headers, method="GET")

        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
        try:
            with urllib.request.urlopen(req, timeout=timeout_sec, context=ctx) as resp:
                sha = hashlib.sha256()
                total = 0
                with open(out_path, "wb") as fh:
                    while True:
                        chunk = resp.read(65536)
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > max_bytes:
                            fh.close()
                            try: os.remove(out_path)
                            except Exception: pass
                            return f"Aborted: download exceeded {max_bytes} bytes."
                        fh.write(chunk)
                        sha.update(chunk)
                return f"Saved: {out_path}\nSize: {total} bytes\nSHA256: {sha.hexdigest()}"
        except urllib.error.HTTPError as e:
            return f"HTTPError {e.code}: {e.reason}"
        except urllib.error.URLError as e:
            return f"URLError: {e.reason}"
        except Exception as e:
            return f"Error: {e}"
