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
| 정리 노트 (Study Notes) | "정리해줘", "정리", "강의 정리", "요약 정리", "make study notes" |
| Data Table | "create table", "organize as data table" |

## 정리 명령어 (Study Notes)

"정리"라고 하면 `generate_study_notes` 도구로 **강의 슬라이드 정리본 스타일**의 노트를 만듭니다.
(기준 예시: 약리학 Chapter 21 항고혈압약물 정리본)

### 출력 구성

1. **표지** – 과목명(한글 + 영문), `Chapter 번호 한글제목 *English Title*`
2. **학습 목표** – 번호 목록, 핵심 키워드 굵게
3. **본문** – 슬라이드 순서대로 `## 소제목` 섹션
   - 줄글 대신 개조식 (`➢` 큰 항목, `-` 세부 항목)
   - 기전은 화살표 연쇄: `Na⁺·수분 배설↑ → 혈액량↓ → 심박출량↓ → BP↓`
   - 어려운 개념 아래 `= 쉬운 말 풀이` 한 줄
4. **표 정리** – 약물/개념 그룹마다 표
   - 단일 그룹: `기전 / 약제 / 효과 / 부작용 / 비고(주의·간호)`
   - 비교: `| 구분 | A | B | C |` (예: ACEi vs ARB vs 레닌억제제, Non-DHP vs DHP)
   - 표 아래 `**공통: ...**` 한 줄 요약, 헷갈리는 개념은 `※` 주의
5. **표기 규칙**
   - 한글 + 영문(약어) 병기: `심박출량 Cardiac Output(CO)`
   - 일반명 + 상품명: `Amlodipine(노바스크)`
   - 계열 어미 굵게: `Capto**pril**`, `Lo**sartan**`, `Amlo**dipine**`, `Ate**nolol**`
   - 시험 핵심(금기, 대표 부작용, 반동 현상 등) 굵게
6. **임상 적용 / 간호** – `| 환자 상황 | 우선 고려 약물 | 이유 |`, 응급 약물 `| 약물 | 투여 | 작용 시간 | 간호 포인트 |`, 환자 안전과 교육
7. **핵심용어** – `용어 (약어): 한 줄 정의`

### 사용 예시

```
이 노트북 정리해줘
21장 항고혈압약물만 정리해줘
정리해줘, 간호 포인트 더 자세히
```

`topic`(정리 범위)과 `extra_instructions`(추가 요청)를 넘길 수 있고, 기본 언어는 한국어(`ko`)입니다.

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
