# ~/.config/shell_gpt/functions/memory_clear.py
import json, os
from typing import List, Optional, Literal
from pydantic import Field
from instructor import OpenAISchema

MEMORY_PATH = os.path.expanduser(
    os.environ.get("SGPT_MEMORY_FILE", "~/.config/shell_gpt/memory.json")
)

class Function(OpenAISchema):
    """
    Clear memories. Delete specific IDs or wipe everything.

    - Provide a list of IDs to delete only those.
    - If no IDs are provided, 'confirm' must be "YES" to delete ALL.
    """

    ids: Optional[List[int]] = Field(
        None, description="IDs to delete. If omitted, all memories will be deleted (requires confirm='YES')."
    )
    confirm: Literal["YES"] = Field(
        ..., description="Type 'YES' to confirm deletion."
    )

    class Config:
        title = "memory_clear"

    @classmethod
    def execute(cls, ids: Optional[List[int]] = None, confirm: str = "YES") -> str:
        if confirm != "YES":
            return "Refused: confirmation is required."

        if not os.path.exists(MEMORY_PATH):
            return "Nothing to delete: memory DB not found."

        try:
            data = json.load(open(MEMORY_PATH, "r", encoding="utf-8"))
            if not isinstance(data, list):
                data = []
        except Exception:
            data = []

        if not data:
            return "Nothing to delete: memory DB is empty."

        if ids:
            ids_set = set(int(x) for x in ids)
            before = len(data)
            data = [e for e in data if int(e.get("id", -1)) not in ids_set]
            deleted = before - len(data)
            json.dump(data, open(MEMORY_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            return f"Deleted {deleted} entrie(s) by ID."
        else:
            # wipe all
            json.dump([], open(MEMORY_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            return "All memories deleted."
