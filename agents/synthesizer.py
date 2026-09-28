from crewai import Agent
from config.llm import get_llm


def create_synthesizer() -> Agent:
    return Agent(
        role="Research Report Synthesizer",
        goal="Produce a concise evidence-based research report.",
        backstory=(
            "You transform verified research evidence into a clear, "
            "professional research report without inventing information."
        ),
        llm=get_llm(1100),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
