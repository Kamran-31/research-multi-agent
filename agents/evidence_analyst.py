from crewai import Agent
from config.llm import get_llm


def create_evidence_analyst() -> Agent:
    return Agent(
        role="Evidence Analysis Specialist",
        goal=(
            "Convert the research dossiers into a concise evidence map "
            "containing claims, supporting sources, contradictions and gaps."
        ),
        backstory=(
            "You are a meticulous evidence analyst. You compare findings "
            "and identify where evidence agrees, conflicts or is insufficient."
        ),
        llm=get_llm(),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
