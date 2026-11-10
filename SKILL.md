# NotebookLM Assistant Skill

This skill enables automated content processing and generation through NotebookLM, converting various content sources into multiple output formats.

## Supported Content Sources

| Source Type | Description |
|-------------|-------------|
| Web Pages | Any URL or web article |
| YouTube Videos | Video transcripts and content |
| Office Documents | Word (.docx), PowerPoint (.pptx), Excel (.xlsx) |
| PDFs | PDF documents |
| eBooks | EPUB files |
| Images | With OCR text extraction |
| Audio Files | With transcription |
| Structured Data | CSV, JSON, XML files |
| Plain Text | Markdown (.md), Text (.txt) |
| ZIP Archives | Compressed file bundles |

## Output Formats

Generate content in various formats using natural language commands:

| Format | Example Commands |
|--------|------------------|
| Podcast | "generate podcast", "create audio discussion" |
| Video | "make a video", "generate video content" |
| PPT Slides | "create slides", "make a presentation", "generate PPT" |
| Mind Map | "create mind map", "generate concept map" |
| Infographic | "make infographic", "create visual summary" |
| Quiz | "generate quiz", "create test questions" |
| Flashcards | "make flashcards", "create study cards" |
| Report | "write report", "generate summary report" |
| Data Table | "create table", "organize as data table" |

## 정리 명령어 (Study Notes)

"정리"는 NotebookLM을 쓰지 않습니다. 강의 자료(PDF·PPT·Word·이미지)를 주고 "정리해줘"라고 하면
Claude가 직접 읽고 강의 슬라이드 정리본 형식으로 만들어 줍니다.
형식과 규칙은 [.claude/skills/study-notes/SKILL.md](.claude/skills/study-notes/SKILL.md)에 있습니다.

## Setup Requirements

### 1. NotebookLM Authentication

Before first use, authenticate with NotebookLM:

```bash
notebooklm login
```

Verify authentication:

```bash
notebooklm list
```

### 2. MCP Server Configuration (Optional)

For extended content source support, configure MCP servers in `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "notebooklm",
      "args": ["mcp"]
    }
  }
}
```

Restart Claude after configuration changes.

## Workflow

1. **Content Detection**: Automatically identify the content source type from user input
2. **Content Extraction**: Retrieve and process content using appropriate tools
   - Direct URL fetch for web pages
   - YouTube transcript extraction for videos
   - Document parsing for Office files/PDFs
   - OCR for images
   - Transcription for audio
3. **Upload to NotebookLM**: Add processed content as notebook source
4. **Generation**: Create requested output format based on user intent
5. **Download**: Save generated outputs to local storage

## Usage Examples

### Generate a podcast from a web article
```
Create a podcast from https://example.com/article
```

### Create slides from a PDF
```
Make a presentation from report.pdf
```

### Generate a mind map from YouTube video
```
Create a mind map from https://youtube.com/watch?v=xxxxx
```

### Create flashcards from a document
```
Generate flashcards from study-guide.docx
```

### Make an infographic from structured data
```
Create an infographic from data.csv
```

## Error Handling

- If authentication fails, run `notebooklm login` again
- For unsupported file types, convert to a supported format first
- Large files may require chunking or compression
- Network errors will prompt automatic retry

## Notes

- Processing time varies based on content size and output type
- Some outputs (like video) may take longer to generate
- Generated files are saved to the current working directory by default
