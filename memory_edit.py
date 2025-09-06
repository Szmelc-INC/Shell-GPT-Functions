# ~/.config/shell_gpt/functions/memory_edit.py
import json, os
from typing import Optional, Literal
from pydantic import Field
from instructor import OpenAISchema

MEMORY_PATH = os.path.expanduser(
    os.environ.get("SGPT_MEMORY_FILE", "~/.config/shell_gpt/memory.json")
)

class Function(OpenAISchema):
    """
    Edit a memory's title and/or summary.

    - summary_mode: how to apply the provided summary text:
        * 'replace'  -> overwrite
        * 'append'   -> add to the end (with a newline)
        * 'prepend'  -> add to the start (with a newline)
    """

    id: int = Field(..., description="ID of the memory to edit.")
    title: Optional[str] = Field(None, description="New title. Leave unset to keep.")
    summary: Optional[str] = Field(None, description="Summary text to apply.")
    summary_mode: Literal["replace", "append", "prepend"] = Field(
        "replace", description="How to apply the new summary text."
    )

    class Config:
        title = "memory_edit"

    @classmethod
    def execute(
        cls,
        id: int,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        summary_mode: str = "replace",
    ) -> str:
        if not os.path.exists(MEMORY_PATH):
            return "Memory DB not found."

        try:
            data = json.load(open(MEMORY_PATH, "r", encoding="utf-8"))
            if not isinstance(data, list):
                return "Corrupt memory DB."
        except Exception:
            return "Could not read memory DB."

        target = None
        for e in data:
            if int(e.get("id", -1)) == int(id):
                target = e
                break

        if not target:
            return f"Memory #{id} not found."

        changed = False

        if title is not None:
            target["title"] = title
            changed = True

        if summary is not None:
            existing = target.get("summary", "")
            if summary_mode == "replace":
                target["summary"] = summary
            elif summary_mode == "append":
                target["summary"] = (existing + ("\n" if existing and not existing.endswith("\n") else "") + summary).rstrip()
            elif summary_mode == "prepend":
                target["summary"] = (summary + ("\n" if summary and not summary.endswith("\n") else "") + existing).rstrip()
            else:
                return f"Invalid summary_mode: {summary_mode}"
            changed = True

        if not changed:
            return "No changes provided."

        json.dump(data, open(MEMORY_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        return f"Updated memory #{id}."
