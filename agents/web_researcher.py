from crewai import Agent
from config.llm import get_llm


def create_web_researcher() -> Agent:
    return Agent(
        role="Web Research Specialist",
        goal="Analyze the supplied web research evidence and extract the most important findings.",
        backstory=(
            "You are a web research analyst. "
            "You evaluate supplied web evidence and identify reliable, "
            "relevant findings without inventing information."
        ),
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
