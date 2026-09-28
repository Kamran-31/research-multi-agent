from crewai import Agent
from config.llm import get_llm


def create_academic_researcher() -> Agent:
    return Agent(
        role="Academic Research Specialist",
        goal="Analyze supplied academic evidence and extract the most relevant findings.",
        backstory=(
            "You are an academic research analyst. "
            "You evaluate scholarly evidence and identify useful findings "
            "while clearly noting limitations."
        ),
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
