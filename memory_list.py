# ~/.config/shell_gpt/functions/memory_list.py
import json, os
from typing import Optional
from pydantic import Field
from instructor import OpenAISchema

MEMORY_PATH = os.path.expanduser(
    os.environ.get("SGPT_MEMORY_FILE", "~/.config/shell_gpt/memory.json")
)

class Function(OpenAISchema):
    """
    List recent memories. Optional substring filter on title/summary.
    """
    query: Optional[str] = Field(None, description="Substring to filter title/summary.")
    limit: int = Field(20, ge=1, le=200, description="Max entries to return.")

    class Config:
        title = "list_memories"

    @classmethod
    def execute(cls, query: Optional[str] = None, limit: int = 20) -> str:
        if not os.path.exists(MEMORY_PATH):
            return "No memories."
        try:
            items = json.load(open(MEMORY_PATH, "r", encoding="utf-8"))
        except Exception:
            return "Could not read memory DB."
        items = sorted(items, key=lambda x: x.get("id", 0), reverse=True)
        out = []
        q = (query or "").lower()
        for it in items:
            line = f"#{it['id']}  {it['created']}  {it['title']}"
            if not q or q in it.get("title","").lower() or q in it.get("summary","").lower():
                out.append(line)
            if len(out) >= limit:
                break
        return "\n".join(out) if out else "No matches."
