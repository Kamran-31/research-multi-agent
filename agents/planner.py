from crewai import Agent

from config.llm import get_llm


def create_planner() -> Agent:
    return Agent(
        role="Research Planning Specialist",
        goal=(
            "Turn the user's research question into a precise evidence-oriented "
            "research plan with clear subquestions and source requirements."
        ),
        backstory=(
            "You are a senior research strategist. You break broad questions "
            "into focused investigative areas and define what evidence the "
            "research team needs to establish."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
