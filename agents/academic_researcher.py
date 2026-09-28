from crewai import Agent
from config.llm import get_llm
from tools.academic_search import academic_search_tool


def create_academic_researcher() -> Agent:
    return Agent(
        role="Academic Research Specialist",
        goal="Find the most relevant scholarly evidence.",
        backstory=(
            "You search academic literature and identify useful "
            "research findings while avoiding unnecessary detail."
        ),
        tools=[academic_search_tool],
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=2,
        verbose=False,
    )
