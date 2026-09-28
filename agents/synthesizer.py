from crewai import Agent
from config.llm import get_llm


def create_synthesizer() -> Agent:
    return Agent(
        role="Research Report Synthesizer",
        goal="Create the final evidence-based research report.",
        backstory="You transform verified evidence into a concise professional report.",
        llm=get_llm(1200),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
