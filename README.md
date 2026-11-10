# NotebookLM MCP for Claude (Desktop & CLI)

A powerful MCP (Model Context Protocol) server that brings Google NotebookLM into Claude Desktop and Claude Code.

## Features

- **Research**: List and create notebooks
- **Content**: Add URLs, text, and files as sources
- **Generation**: Create Podcasts, Videos, Slides, Mind Maps, Infographics, Quizzes, Flashcards, and Reports
- **Natural Interaction**: Chat directly with your sources using Claude's reasoning

---

## Prerequisites

### 1. Install uv (Python Package Manager)

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
# Using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew (macOS)
brew install uv
```

Default install location: `~/.local/bin/uv`

</details>

<details>
<summary><strong>Windows</strong></summary>

```powershell
# Using PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with Scoop
scoop install uv

# Or with winget
winget install --id=astral-sh.uv -e
```

Default install location: `%USERPROFILE%\.local\bin\uv.exe`

</details>

Verify installation:
```bash
uv --version
```

### 2. Clone and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/alfredang/notebooklm-mcp.git

# Navigate to the project folder
cd notebooklm-mcp

# Install dependencies (includes notebooklm-py and fastmcp)
uv sync
```

This will:
- Create a `.venv` virtual environment
- Install **notebooklm-py** (Python client for NotebookLM API)
- Install **fastmcp** (MCP server framework)

> **Note:** These dependencies are required for both Claude Desktop and Claude Code.

---

## Step 1: Authenticate with NotebookLM

NotebookLM uses browser-based authentication. You must login once to save your session cookies.

```bash
cd notebooklm-mcp
uv run notebooklm login
```

**What happens:**
1. A browser window will open automatically
2. Log in to your Google account
3. Navigate to NotebookLM if not redirected automatically
4. Wait until the terminal displays **"Success"**
5. Close the browser

**Verify authentication:**
```bash
uv run python -c "
from notebooklm import NotebookLMClient
import asyncio
async def test():
    client = await NotebookLMClient.from_storage()
    async with client:
        notebooks = await client.notebooks.list()
        print(f'Authenticated! Found {len(notebooks)} notebooks.')
asyncio.run(test())
"
```

You should see: `Authenticated! Found X notebooks.`

---

## Step 2: Test the MCP Server

Before configuring Claude, verify the server starts correctly:

```bash
cd notebooklm-mcp
uv run python server.py
```

**Expected output:**
```
Starting NotebookLM MCP server...
NotebookLM client initialized successfully
Starting MCP server 'NotebookLM' with transport 'stdio'
```

Press `Ctrl+C` (or `Cmd+C` on Mac) to stop the server after confirming it works.

---

## Step 3: Setup for Claude Desktop

### 3.1 Find Your Paths

You'll need two paths for the configuration:

**Find your `uv` path:**

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
which uv
```
Example output: `/Users/yourname/.local/bin/uv`

</details>

<details>
<summary><strong>Windows</strong></summary>

```powershell
where uv
```
Example output: `C:\Users\yourname\.local\bin\uv.exe`

</details>

**Find your project path:**

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
cd notebooklm-mcp && pwd
```
Example output: `/Users/yourname/projects/notebooklm-mcp`

</details>

<details>
<summary><strong>Windows</strong></summary>

```powershell
cd notebooklm-mcp; (Get-Location).Path
```
Example output: `C:\Users\yourname\projects\notebooklm-mcp`

</details>

### 3.2 Open the Config File

**From Claude Desktop (Recommended):**

1. Open Claude Desktop
2. Go to **Settings** (gear icon) → **Developer** → **Edit Config**
3. This opens `claude_desktop_config.json` in your default editor

**Or manually:**

<details>
<summary>macOS path</summary>

`~/Library/Application Support/Claude/claude_desktop_config.json`

</details>

<details>
<summary>Windows path</summary>

`%APPDATA%\Claude\claude_desktop_config.json`

</details>

### 3.3 Add the MCP Server Configuration

> **Important:** Replace `<UV_PATH>` and `<PROJECT_PATH>` with your actual paths from Step 3.1

<details>
<summary><strong>macOS / Linux Configuration</strong></summary>

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "<UV_PATH>",
      "args": [
        "--directory",
        "<PROJECT_PATH>",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

**Example with real paths:**
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "/Users/yourname/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/yourname/projects/notebooklm-mcp",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

</details>

<details>
<summary><strong>Windows Configuration</strong></summary>

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "<UV_PATH>",
      "args": [
        "--directory",
        "<PROJECT_PATH>",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

**Example with real paths:**
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "C:\\Users\\yourname\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:\\Users\\yourname\\projects\\notebooklm-mcp",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

> **Note:** On Windows, use double backslashes (`\\`) in JSON paths.

</details>

### 3.4 Restart Claude Desktop

| Platform | How to Restart |
|----------|----------------|
| **macOS** | Press `Cmd+Q` to fully quit, then reopen |
| **Windows** | Right-click tray icon → Quit, then reopen |

Look for the **hammer icon** in the chat input area - this indicates MCP tools are available.

### 3.5 Verify Connection

In Claude Desktop, type:
```
List my NotebookLM notebooks
```

Claude should use the `list_notebooks` tool and display your notebooks.

---

## Step 4: Setup for Claude Code (CLI)

> **Prerequisites:** Complete Steps 1-2 first (install dependencies with `uv sync` and authenticate with `uv run notebooklm login`).

### 4.1 Add the MCP Server

Replace `<PROJECT_PATH>` with your actual project path:

<details>
<summary><strong>macOS / Linux</strong></summary>

```bash
claude mcp add notebooklm -- uv --directory <PROJECT_PATH> run python server.py
```

**Example:**
```bash
claude mcp add notebooklm -- uv --directory /Users/yourname/projects/notebooklm-mcp run python server.py
```

</details>

<details>
<summary><strong>Windows</strong></summary>

```powershell
claude mcp add notebooklm -- uv --directory <PROJECT_PATH> run python server.py
```

**Example:**
```powershell
claude mcp add notebooklm -- uv --directory C:\Users\yourname\projects\notebooklm-mcp run python server.py
```

</details>

### 4.2 Verify the Server is Added

```bash
claude mcp list
```

You should see `notebooklm` in the list.

### 4.3 Test in Claude Code

Start a new Claude Code session:
```bash
claude
```

Then ask:
```
List my NotebookLM notebooks
```

---

## Usage Examples

Once configured, use natural language commands in Claude Desktop or Claude Code:

| Task | Example Command |
|------|-----------------|
| List notebooks | "Show me all my NotebookLM notebooks" |
| Create notebook | "Create a new notebook called 'Research Project'" |
| Add URL source | "Add this URL to my notebook: https://example.com/article" |
| Generate podcast | "Generate a podcast for notebook ID xyz123" |
| Create slides | "Make a slide deck from my 'Research Project' notebook" |
| Generate mind map | "Create a mind map for notebook abc456" |
| Create quiz | "Generate a quiz based on my notebook sources" |
| Make flashcards | "Create study flashcards from this notebook" |
| 정리 노트 | "이 노트북 정리해줘", "21장만 정리해줘" |

### 정리 명령어

"정리해줘"라고 하면 `generate_study_notes`가 강의 슬라이드 정리본 스타일의 노트를 만듭니다:
표지(과목·장 제목) → 학습 목표 → 슬라이드 순서 섹션(개조식, `→ ↑ ↓` 기전 표기, `기전/약제/효과/부작용/비고` 표와 비교표) → 임상 적용·간호 → 환자 교육 → 핵심용어.
자세한 형식은 [SKILL.md](SKILL.md#정리-명령어-study-notes)를 참고하세요.

---

## Available Tools

| Tool | Description |
|------|-------------|
| `list_notebooks` | List all notebooks in your account |
| `create_notebook` | Create a new notebook |
| `add_source_url` | Add a website URL as a source |
| `add_source_text` | Add raw text as a source |
| `ask_notebook` | Ask a question based on notebook sources |
| `get_notebook_summary` | Get summary and key insights |
| `generate_audio_overview` | Generate a podcast-style audio |
| `generate_video_overview` | Generate a video overview |
| `generate_slide_deck` | Generate PowerPoint-style slides |
| `generate_mind_map` | Generate an interactive mind map |
| `generate_infographic` | Generate a visual infographic |
| `generate_quiz` | Generate quiz questions |
| `generate_flashcards` | Generate study flashcards |
| `generate_summary_report` | Generate a briefing document |
| `generate_study_notes` | "정리" – lecture-style study notes (Korean by default) |
| `generate_data_table` | Extract data into a table |

---

## Troubleshooting

### "Server disconnected" or "Failed to spawn process"

**Cause**: Claude Desktop can't find `uv` because it doesn't inherit your shell's PATH.

**Solution**: Use the **full absolute path** to `uv` in the config (see Step 3.1).

---

### "Command not found: uv"

<details>
<summary><strong>macOS / Linux</strong></summary>

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

</details>

<details>
<summary><strong>Windows</strong></summary>

Add to your PATH:
1. Open System Properties → Environment Variables
2. Under "User variables", edit `Path`
3. Add: `%USERPROFILE%\.local\bin`
4. Restart your terminal

</details>

---

### MCP Server Not Appearing in Claude Desktop

**Cause**: Invalid JSON in config file or Claude not restarted properly.

**Solution**:
1. Validate your JSON at https://jsonlint.com/
2. Ensure no trailing commas in the JSON
3. Fully quit and reopen Claude Desktop

---

### "NotebookLM client not initialized"

**Cause**: Server started before authentication was complete.

**Solution**:
1. Run `uv run notebooklm login` first
2. Restart Claude Desktop or re-add the MCP server in Claude Code

---

### Check Claude Desktop Logs

<details>
<summary><strong>macOS</strong></summary>

```bash
# View recent logs
tail -100 ~/Library/Logs/Claude/mcp*.log

# Or open in Finder
open ~/Library/Logs/Claude/
```

</details>

<details>
<summary><strong>Windows</strong></summary>

```powershell
# View logs folder
explorer "$env:APPDATA\Claude\logs"
```

</details>

---

### Remove and Re-add MCP Server (Claude Code)

If issues persist:
```bash
claude mcp remove notebooklm
claude mcp add notebooklm -- uv --directory <PROJECT_PATH> run python server.py
```

---

## Updating

To update the NotebookLM library:
```bash
cd notebooklm-mcp
uv sync --upgrade
```

---

## Project Structure

```
notebooklm-mcp/
├── server.py          # MCP server implementation
├── pyproject.toml     # Project dependencies
├── README.md          # This file
├── SKILL.md           # Claude Code skill definition
└── .venv/             # Virtual environment (auto-created)
```

---

## License

MIT License
