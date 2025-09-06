# Shell-GPT-Functions
> Some custom functions for Shell GPT

## Setup
> Drop `.py` files into `~/.config/shell_gpt/functions` and run `sgpt --install-functions`

---

# Functions

> # Persistent Memory Functions
>
> This adds simple persistent memory to Shell GPT.  
> You can **remember**, **read**, **list**, **edit**, and **clear** memories across sessions.
>
> ---
>
> ## Installation
>
> Files:
>
> - `remember.py`
> - `memory.py`
> - `memory_list.py`
> - `memory_edit.py`
> - `memory_clear.py`
>
> ---
>
> ## Usage Examples
>
> ### Remember
>
> ```bash
> # Run a command and remember its output
> sgpt "Run ls -l and remember output"
>
> # Remember contents of a file
> sgpt "Remember contents of ~/summary.md"
>
> # Remember a free-form note
> sgpt "Remember that the project uses Python 3.12"
> ```
>
> ### Memory
>
> ```bash
> # Read a memory by ID
> sgpt "Read memory 1"
>
> # Use a memory in a new query
> sgpt "Memory 1, explain what this means"
> ```
>
> ### List Memories
>
> ```bash
> # List recent memories
> sgpt "List memories"
>
> # Search for memories about logs
> sgpt "List memories about logs"
> ```
>
> ### Edit Memories
>
> ```bash
> # Edit memory title
> sgpt "Edit memory 5 title to 'System summary'"
>
> # Replace memory contents
> sgpt "Edit memory 5 contents to 'Shortened summary text'"
>
> # Append to memory contents
> sgpt "Edit memory 5 contents, add 'Extra details'"
> ```
>
> ### Clear Memories
>
> ```bash
> # Clear a specific memory
> sgpt "Clear memory 5"
>
> # Clear multiple memories
> sgpt "Clear memory 2 and 3"
>
> # Clear all memories
> sgpt "Clear all memories"
> ```
>
> ---
>
> ## Notes
>
> - All data is stored locally in:
>   ```
>   ~/.config/shell_gpt/memory.json
>   ```
> - Each memory has an incremental `id` and optional `title`.
> - Summaries auto-trim long outputs for easier use.
>
> ---
>
> # Web Functions
>
> These add simple web browsing abilities to Shell GPT.  
> You can **fetch pages**, **download files**, **extract links**, and **convert HTML to text**.
>
> ---
>
> ## Installation
>
> Files:
>
> - `web_get.py`
> - `web_download.py`
> - `web_extract_links.py`
> - `web_text.py`
>
> ---
>
> ## Usage Examples
>
> ### Fetch Page
>
> ```bash
> # Fetch a page and show headers + preview
> sgpt "Fetch https://example.com and show me headers"
>
> # Short preview of a page
> sgpt "Get https://example.com, short preview"
> ```
>
> ### Download File
>
> ```bash
> # Download a file to /tmp
> sgpt "Download https://example.com/file.zip to /tmp/file.zip"
> ```
>
> ### Extract Links
>
> ```bash
> # List all links on a page
> sgpt "List all links on https://example.com"
> ```
>
> ### Convert to Text
>
> ```bash
> # Fetch a page and return plain text
> sgpt "Fetch https://example.com and give me the plain text"
> ```
>
> ---
>
> ## Notes
>
> - Downloads are capped in size (default 50 MB) for safety.
> - SHA-256 hash is provided for downloaded files.
> - User-Agent is set to a default but can be overridden if needed.
> - All output is truncated to keep responses manageable.

---

# Note
> `execute_shell.py` is a default function to execute shell commands (made by Shell GPT author)

