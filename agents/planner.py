from crewai import Agent
from config.llm import get_llm


def create_planner() -> Agent:
    return Agent(
        role="Research Planning Specialist",
        goal="Create a compact research plan for the user's question.",
        backstory=(
            "You are an expert research strategist. "
            "Break complex questions into focused research areas "
            "without unnecessary explanation."
        ),
        llm=get_llm(500),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
