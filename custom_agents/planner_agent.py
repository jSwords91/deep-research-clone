from pydantic import BaseModel

from agents import Agent, ModelSettings

PLANNER_AGENT_PROMPT = (
    "You are a helpful research assistant. Given a query, come up with a set of web searches "
    "to perform to best answer the query. Output between 5 and 20 terms to query for."
)

CRITIQUE_AGENT_PROMPT = (
    "You are a helpful assistant that critiques the search plan and suggests improvements in order to answer the user's query as efficiently as possible."
)

class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""

class Improvements(BaseModel):
    improvements: list[str]
    "A list of improvements to the search plan."

class Critique(BaseModel):
    critique: str
    "The critique of the search plan."

    improvements: list[Improvements]
    "A list of improvements to the search plan."

    improved_plan: WebSearchPlan
    "The improved search plan."


critiquing_agent = Agent(
    name="CritiquingAgent",
    instructions=CRITIQUE_AGENT_PROMPT,
    model="o3-mini",
    output_type=WebSearchPlan,
)

planner_agent = Agent(
    name="PlannerAgent",
    instructions=PLANNER_AGENT_PROMPT,
    model="gpt-5",
    output_type=WebSearchPlan,
    model_settings=ModelSettings(
        tool_choice="required"
    ),
    tools=[
        critiquing_agent.as_tool(
            tool_name="critique_search_plan",
            tool_description="Critique the search plan and suggest improvements to answer the user's query as efficiently as possible.",
        )
    ],
)
