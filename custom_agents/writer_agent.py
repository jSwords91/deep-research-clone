from pydantic import BaseModel
from agents import Agent

WRITER_AGENT_PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words, with full citations."
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


writer_agent = Agent(
    name="WriterAgent",
    instructions=WRITER_AGENT_PROMPT,
    model="o3-mini",
    output_type=ReportData,
)
