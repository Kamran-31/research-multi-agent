from crewai import Agent
from config.llm import get_llm
from tools.web_search import web_search_tool


def create_fact_checker() -> Agent:
    return Agent(
        role="Fact Verification Specialist",
        goal="Verify only the most important claims in the evidence map.",
        backstory=(
            "You verify statistics, dates, important claims and "
            "potentially questionable statements using reliable sources."
        ),
        tools=[web_search_tool],
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=2,
        verbose=False,
    )
