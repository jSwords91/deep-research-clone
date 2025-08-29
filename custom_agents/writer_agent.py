from pydantic import BaseModel
from agents import Agent, function_tool, ModelSettings
from pathlib import Path
import json

WRITER_AGENT_PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words, with full citations."
    "You should use the write_markdown tool to write the report to a file."
)

class Citation(BaseModel):
    source_name: str | None = None
    "The name of the source of the citation."

    source_url: str | None = None
    "The url of the source of the citation."

    page_number: int | None = None
    "The page number of the citation."

class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""

    citations: list[Citation]
    """A list of citations for the report."""

ROOT_DIR: Path = Path(__file__).resolve().parent  # repository root


def repo_path(rel: str | Path) -> Path:
    """Return an absolute Path inside the repository given a relative string."""
    return (ROOT_DIR / rel).resolve()


def outputs_dir() -> Path:
    """Return the global `outputs/` folder, creating it if needed."""
    out = repo_path("outputs")
    out.mkdir(parents=True, exist_ok=True)
    return out

def output_file(name: str | Path, *, make_parents: bool = True) -> Path:
    """Return an absolute Path under the shared outputs/ directory.

    If *name* already starts with the string "outputs/", that prefix is removed
    to avoid accidentally nesting a second outputs folder (e.g.
    `outputs/outputs/foo.png`).  Absolute paths are returned unchanged.
    """

    path = Path(name)

    if path.is_absolute():
        return path

    # Strip leading "outputs/" if present
    if path.parts and path.parts[0] == "outputs":
        path = Path(*path.parts[1:])

    final = outputs_dir() / path

    if make_parents:
        final.parent.mkdir(parents=True, exist_ok=True)

    return final

@function_tool
def write_markdown(filename: str, content: str) -> str:
    """Write `content` to `outputs/filename` and return confirmation JSON."""
    if not filename.endswith(".md"):
        filename += ".md"
    path = output_file(filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return json.dumps({"file": filename})


writer_agent = Agent(
    name="WriterAgent",
    instructions=WRITER_AGENT_PROMPT,
    model="o3-mini",
    output_type=ReportData,
    tools=[write_markdown],
    model_settings=ModelSettings(tool_choice="required"),
)
