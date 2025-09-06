# ~/.config/shell_gpt/functions/memory.py
import json, os
from pydantic import Field
from instructor import OpenAISchema

MEMORY_PATH = os.path.expanduser(
    os.environ.get("SGPT_MEMORY_FILE", "~/.config/shell_gpt/memory.json")
)

class Function(OpenAISchema):
    """
    Retrieve a previously saved memory by ID.
    """
    id: int = Field(..., description="Memory ID to fetch.")

    class Config:
        title = "memory"

    @classmethod
    def execute(cls, id: int) -> str:
        if not os.path.exists(MEMORY_PATH):
            return f"No memory DB at {MEMORY_PATH}"
        try:
            data = json.load(open(MEMORY_PATH, "r", encoding="utf-8"))
        except Exception:
            return "Could not read memory DB."
        for it in data:
            if it.get("id") == id:
                return f"[Memory #{id}: {it.get('title')}] {it.get('summary')}"
        return f"Memory #{id} not found."
