from crewai import Agent
from config.llm import get_llm


def create_academic_researcher() -> Agent:
    return Agent(
        role="Academic Research Specialist",
        goal="Analyze supplied academic evidence.",
        backstory="You extract relevant findings from scholarly research.",
        llm=get_llm(600),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
