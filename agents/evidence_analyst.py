from crewai import Agent
from config.llm import get_llm


def create_evidence_analyst() -> Agent:
    return Agent(
        role="Evidence Analysis Specialist",
        goal="Compare research findings and identify supported claims, contradictions and gaps.",
        backstory=(
            "You analyze research evidence objectively. "
            "You do not introduce information that is not present in the supplied evidence."
        ),
        llm=get_llm(700),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
