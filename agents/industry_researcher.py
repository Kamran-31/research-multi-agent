from crewai import Agent
from config.llm import get_llm


def create_industry_researcher() -> Agent:
    return Agent(
        role="Industry Research Specialist",
        goal="Analyze supplied industry evidence.",
        backstory="You extract real-world industry findings.",
        llm=get_llm(350),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
