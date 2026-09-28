from crewai import Agent
from config.llm import get_llm


def create_fact_checker() -> Agent:
    return Agent(
        role="Fact Checker",
        goal="Check important claims against supplied evidence.",
        backstory="You identify supported, conflicting and unverified claims.",
        llm=get_llm(700),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
