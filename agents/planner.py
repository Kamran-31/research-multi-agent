from crewai import Agent
from config.llm import get_llm


def create_planner() -> Agent:
    return Agent(
        role="Research Planning Specialist",
        goal="Create a concise research plan.",
        backstory="You turn a research question into focused subquestions.",
        llm=get_llm(400),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
