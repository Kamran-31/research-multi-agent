from crewai import Agent
from config.llm import get_llm


def create_planner() -> Agent:
    return Agent(
        role="Research Planning Specialist",
        goal=(
            "Convert the user's question into a concise research plan "
            "with focused subquestions and evidence requirements."
        ),
        backstory=(
            "You are a research strategist. You identify the exact questions "
            "that need to be answered and the evidence required to answer them."
        ),
        llm=get_llm(),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
