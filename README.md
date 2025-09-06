# Shell-GPT-Functions
> Some custom functions for Shell GPT

# Setup
> Drop `.py` files into `~/.config/shell_gpt/functions` and run `sgpt --install-functions`

---

# Functions

> ## Persistent Memory
>
> **Files:** `remember.py`, `memory.py`, `memory_list.py`
>
> These add simple persistent memory commands to Shell GPT.
>
> ---
>
> ## Remember
>
> Save command output, file content, or notes into memory.
>
> Examples:
>
> ```bash
> # Run a command and remember its output
> sgpt "Run ls -l and remember output"
>
> # Remember contents of a file
> sgpt "Remember contents of ~/summary.md"
>
> # Save a free-form note
> sgpt "Remember that the project uses Python 3.12"
> ```
>
> ---
>
> ## Memory
>
> Fetch a saved memory by ID:
>
> ```bash
> sgpt "Read memory 1"
> sgpt "Use memory 1 to explain what this output means"
> ```
>
> ---
>
> ## List Memories
>
> List or search stored entries:
>
> ```bash
> sgpt "List memories"
> sgpt "List memories about logs"
> ```
>
> ---
>
> ## Notes
>
> - Data is stored in `~/.config/shell_gpt/memory.json`
> - Each memory has an incremental `id` and optional `title`
