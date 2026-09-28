from crewai import Agent
from config.llm import get_llm
from tools.web_search import web_search_tool


def create_web_researcher() -> Agent:
    return Agent(
        role="Web Research Specialist",
        goal="Find concise, reliable current web evidence.",
        backstory=(
            "You investigate official sources, institutions, "
            "primary sources and reputable reporting."
        ),
        tools=[web_search_tool],
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=2,
        verbose=False,
    )
