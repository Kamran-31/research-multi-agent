from crewai import Agent
from config.llm import get_llm


def create_web_researcher() -> Agent:
    return Agent(
        role="Web Research Specialist",
        goal="Analyze supplied web evidence.",
        backstory="You extract important findings from web research.",
        llm=get_llm(600),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
