# ~/.config/shell_gpt/functions/remember.py
import json, os, shlex, subprocess
from datetime import datetime
from typing import Optional, Literal
from pydantic import Field
from instructor import OpenAISchema

MEMORY_PATH = os.path.expanduser(
    os.environ.get("SGPT_MEMORY_FILE", "~/.config/shell_gpt/memory.json")
)

def _load() -> list:
    if os.path.exists(MEMORY_PATH):
        try:
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def _save(items: list) -> None:
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    tmp = MEMORY_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MEMORY_PATH)

def _summarise(text: str, max_lines: int = 24) -> str:
    lines = [ln.rstrip() for ln in text.strip().splitlines()]
    if len(lines) <= max_lines:
        return "\n".join(lines)
    head = lines[: int(max_lines * 0.6)]
    tail = lines[- int(max_lines * 0.4) :]
    return "\n".join(head + ["…", *tail])

class Function(OpenAISchema):
    """
    Remember important information by summarising one of:
    - a shell command output (mode="command"),
    - a local file content (mode="file"),
    - a free-text note (mode="text").

    The summary is stored with an auto-incremented ID for later retrieval.
    """

    mode: Literal["command", "file", "text"] = Field(..., description="What to remember.")
    content: str = Field(
        ...,
        example="du -sh /var/log",
        description="Shell command (mode=command), file path (mode=file), or note text (mode=text).",
    )
    title: Optional[str] = Field(None, description="Optional short title for the memory entry.")

    class Config:
        title = "remember"

    @classmethod
    def execute(cls, mode: str, content: str, title: Optional[str] = None) -> str:
        raw = ""
        if mode == "command":
            try:
                if any(ch in content for ch in ["|", ";", "&", "$(", "`", "*", ">","<"]):
                    p = subprocess.run(["bash", "-lc", content], capture_output=True, text=True)
                else:
                    p = subprocess.run(shlex.split(content), capture_output=True, text=True)
                raw = f"$ {content}\n# exit: {p.returncode}\n\n{p.stdout}\n{p.stderr}"
            except Exception as e:
                raw = f"$ {content}\n# error: {e}"
            default_title = f"Command: {content}"

        elif mode == "file":
            path = os.path.expanduser(content)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
                raw = f"# file: {path}\n\n{text}"
            except Exception as e:
                raw = f"# file: {path}\n# error: {e}"
            default_title = f"File: {os.path.basename(path)}"

        elif mode == "text":
            raw = content
            default_title = "Note"

        else:
            return f"Unsupported mode: {mode}"

        summary = _summarise(raw)
        items = _load()
        new_id = max([it.get("id", 0) for it in items], default=0) + 1
        entry = {
            "id": new_id,
            "created": datetime.utcnow().isoformat() + "Z",
            "title": title or default_title,
            "summary": summary,
            "raw_len": len(raw),
        }
        items.append(entry)
        _save(items)
        return f"Saved memory #{new_id} — {entry['title']}\n{entry['summary']}"
