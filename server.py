import logging
import sys
from contextlib import asynccontextmanager
from fastmcp import FastMCP
from notebooklm import NotebookLMClient, ReportFormat

# Configure logging to stderr (stdout is used for MCP protocol)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Client instance (singleton for the session)
_client = None
_client_context = None

@asynccontextmanager
async def lifespan(_app):
    """Initialize NotebookLM client on server startup."""
    global _client, _client_context
    logger.info("Starting NotebookLM MCP server...")
    try:
        _client = await NotebookLMClient.from_storage()
        _client_context = await _client.__aenter__()
        logger.info("NotebookLM client initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to initialize NotebookLM client: {e}")
        logger.error("Please run 'uv run notebooklm login' to authenticate.")
        raise
    finally:
        if _client:
            try:
                await _client.__aexit__(None, None, None)
                logger.info("NotebookLM client closed")
            except Exception as e:
                logger.error(f"Error closing client: {e}")

# Initialize FastMCP server with lifespan
mcp = FastMCP("NotebookLM", lifespan=lifespan)

async def get_client():
    global _client
    if _client is None:
        raise RuntimeError("NotebookLM client not initialized. Please restart the server.")
    return _client

@mcp.tool()
async def list_notebooks():
    """List all notebooks in your NotebookLM account."""
    client = await get_client()
    notebooks = await client.notebooks.list()
    return [{"id": nb.id, "title": nb.title, "source_count": nb.source_count} for nb in notebooks]

@mcp.tool()
async def create_notebook(title: str):
    """Create a new notebook with the given title."""
    client = await get_client()
    notebook = await client.notebooks.create(title)
    return {"id": notebook.id, "title": notebook.title}

@mcp.tool()
async def add_source_url(notebook_id: str, url: str):
    """Add a website URL as a source to a notebook."""
    client = await get_client()
    source = await client.sources.add_url(notebook_id, url)
    return {"id": source.id, "title": source.title}

@mcp.tool()
async def add_source_text(notebook_id: str, title: str, text: str):
    """Add raw text as a source to a notebook."""
    client = await get_client()
    source = await client.sources.add_text(notebook_id, title, text)
    return {"id": source.id, "title": source.title}

@mcp.tool()
async def ask_notebook(notebook_id: str, question: str):
    """Ask a question based on the sources in a specific notebook."""
    client = await get_client()
    result = await client.chat.ask(notebook_id, question)
    return {"answer": result.text, "sources": [s.title for s in result.sources]}

@mcp.tool()
async def get_notebook_summary(notebook_id: str):
    """Get the summary and key insights of a notebook."""
    client = await get_client()
    # Using chat to get summary if there's no direct summary API
    result = await client.chat.ask(notebook_id, "Please provide a comprehensive summary and key insights of this notebook.")
    return {"summary": result.text}

@mcp.tool()
async def generate_video_overview(notebook_id: str, instructions: str = "Create an engaging video overview of these sources."):
    """
    Generate a Video Overview artifact in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_video(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_audio_overview(notebook_id: str, instructions: str = "Create a deep dive podcast-style overview."):
    """
    Generate an Audio Overview (Deep Dive podcast) in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_audio(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_slide_deck(notebook_id: str, instructions: str = "Create a comprehensive slide deck."):
    """
    Generate a Slide Deck (PowerPoint style) in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_slide_deck(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_mind_map(notebook_id: str):
    """
    Generate an interactive Mind Map in NotebookLM.
    This creates a mind map and saves it as a note.
    """
    client = await get_client()
    result = await client.artifacts.generate_mind_map(notebook_id)
    return {"note_id": result.get("note_id"), "status": "Mind map generated and saved to notes."}

@mcp.tool()
async def generate_infographic(notebook_id: str, instructions: str = "Create an informative infographic."):
    """
    Generate an Infographic in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_infographic(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_quiz(notebook_id: str, instructions: str = "Create a quiz based on these sources."):
    """
    Generate a Quiz in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_quiz(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_flashcards(notebook_id: str, instructions: str = "Create study flashcards."):
    """
    Generate Flashcards in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_flashcards(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

@mcp.tool()
async def generate_summary_report(notebook_id: str, instructions: str = "Create a briefing document."):
    """
    Generate a Summary Report (Briefing Doc) in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_report(notebook_id, custom_prompt=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

# "정리" 명령어의 출력 형식.
# 강의 슬라이드 정리본(예: 약리학 21장 항고혈압약물) 스타일을 그대로 따른다.
STUDY_NOTES_PROMPT = """\
소스(강의 슬라이드/교재)를 시험 공부용 '강의 정리 노트'로 정리해 주세요. 한국어로 작성합니다.
아래 형식을 반드시 따르세요.

[1. 표지]
- 첫 줄: 과목명 (한글 + 영문). 예) 약리학 Pharmacology
- 장 제목: "# Chapter 번호 한글제목 *English Title*" 형식. 예) # Chapter 21 항고혈압약물 *Antihypertensive Drugs*

[2. 학습 목표]
- "## 학습 목표" 아래 번호 목록(1. 2. 3. ...)으로 작성
- 각 목표의 핵심 키워드는 **굵게** 표시

[3. 본문 - 슬라이드 순서대로]
- 소스의 흐름(슬라이드 순서)을 유지하고, 주제마다 "## 소제목"으로 나눕니다
- 줄글 금지. 짧은 개조식으로 씁니다: 큰 항목은 "➢", 세부 항목은 "-"
- 기전·인과관계는 화살표 연쇄로 표현하고 증감은 ↑ ↓ 기호를 씁니다
  예) Na⁺·수분 배설↑ → 혈액량↓ → 심박출량↓ → BP↓
- 중요한 공식은 한 줄로 따로 씁니다. 예) Blood pressure = CO Ⅹ Peripheral resistance
- 어려운 개념 바로 아래에는 "= 쉬운 말 풀이"를 한 줄 덧붙입니다
  예) 심근수축력·심박수↓  = 심장이 일을 덜 하게 함

[4. 표 정리 (가장 중요)]
- 약물(또는 질환/개념) 그룹마다 표로 정리합니다
- 단일 그룹 표: 왼쪽 열 = 항목, 오른쪽 열 = 내용
  항목 순서: 기전 / 약제 / 효과(적응증) / 부작용 / 비고(주의·간호)
- 여러 그룹 비교 표: 첫 열 "구분", 나머지 열 = 비교 대상
  예) | 구분 | ACEi (-pril) | ARB (-sartan) | 레닌억제제 |
       행: 약제 / 차단 지점 / 부작용 / 임신 / 장점
- 하위 분류가 있으면 비교 표로 나눕니다 (예: CCB → Non-DHP vs DHP, 이뇨제 → Thiazide vs Loop vs 칼륨보존)
- 표 바로 아래에 공통점·핵심을 굵은 한 줄로 요약합니다
  예) **공통: 세동맥 확장 → 말초저항↓ → BP↓ / 자몽주스와 함께 복용 금지**
- 헷갈리기 쉬운 개념은 "※"로 시작하는 한 줄 주의를 붙입니다

[5. 표기 규칙]
- 용어는 한글과 영문(약어)을 함께 씁니다. 예) 심박출량 Cardiac Output(CO), 안지오텐신 전환효소 억제제(ACEi)
- 약물명은 영문 일반명을 쓰고 대표 상품명을 괄호로 병기합니다. 예) Amlodipine(노바스크), Furosemide(Lasix)
- 같은 계열 약물의 공통 어미는 굵게 표시해 암기를 돕습니다. 예) Capto**pril**, Lo**sartan**, Amlo**dipine**, Ate**nolol**, Pra**zosin**
- 시험에 나올 핵심(금기, 대표 부작용, 첫 용량 효과, 반동 현상, 임의 중단 금지 등)은 **굵게** 표시합니다
- 자주 쓰는 약어(HT, BP, HR, SV, CO, IV 등)는 처음 나올 때만 풀어 쓰고 이후 약어로 씁니다

[6. 임상 적용 / 간호]
- 상황별 우선 선택을 표로 정리합니다: | 환자 상황 | 우선 고려 약물 | 이유 |
- 응급·투여 약물은 | 약물 | 투여 | 작용 시간 | 간호 포인트 | 표로 정리합니다
- "환자 안전과 교육" 섹션: 모니터링, 부작용 교육, 보고해야 할 증상, 병용 주의, 순응도를 ➢ 개조식으로 씁니다

[7. 핵심용어]
- 마지막에 "## 핵심용어" 섹션을 두고 "용어 (약어): 한 줄 정의" 목록으로 정리합니다

소스에 없는 내용은 지어내지 말고, 소스의 수치·약물명·용량은 그대로 옮기세요.
"""


@mcp.tool()
async def generate_study_notes(
    notebook_id: str,
    topic: str = "",
    extra_instructions: str = "",
    language: str = "ko",
):
    """
    '정리' 명령어: 노트북 소스를 시험 공부용 강의 정리 노트로 만듭니다.
    Use this when the user says "정리해줘", "정리", "강의 정리", "요약 정리", "make study notes".

    Output style: 표지(과목/장 제목) → 학습 목표 → 슬라이드 순서 섹션
    (개조식 + 화살표 기전 + 비교표: 기전/약제/효과/부작용/비고) → 임상 적용·간호 →
    환자 교육 → 핵심용어. Key points in bold, Korean/English terms side by side.

    Args:
        notebook_id: The notebook ID.
        topic: Optional chapter/topic to focus on (e.g. "21장 항고혈압약물").
        extra_instructions: Optional extra requests appended to the format prompt.
        language: Output language code (default "ko").
    """
    client = await get_client()
    prompt = STUDY_NOTES_PROMPT
    if topic:
        prompt += f"\n정리 범위/주제: {topic}\n"
    if extra_instructions:
        prompt += f"\n추가 요청: {extra_instructions}\n"
    status = await client.artifacts.generate_report(
        notebook_id,
        report_format=ReportFormat.CUSTOM,
        language=language,
        custom_prompt=prompt,
    )
    return {"task_id": status.task_id, "status": "정리 노트 생성을 시작했습니다. NotebookLM Studio에서 확인하세요."}

@mcp.tool()
async def generate_data_table(notebook_id: str, instructions: str = "Extract key data into a table."):
    """
    Generate a Data Table artifact in NotebookLM.
    """
    client = await get_client()
    status = await client.artifacts.generate_data_table(notebook_id, instructions=instructions)
    return {"task_id": status.task_id, "status": "Task started. Check NotebookLM studio."}

if __name__ == "__main__":
    mcp.run()
