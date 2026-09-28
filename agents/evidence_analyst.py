from crewai import Agent
from config.llm import get_llm


def create_evidence_analyst() -> Agent:
    return Agent(
        role="Evidence Analyst",
        goal="Identify supported claims, contradictions and evidence gaps.",
        backstory="You compare research evidence objectively.",
        llm=get_llm(500),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
