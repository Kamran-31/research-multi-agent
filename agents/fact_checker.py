from crewai import Agent
from config.llm import get_llm


def create_fact_checker() -> Agent:
    return Agent(
        role="Fact Verification Specialist",
        goal="Evaluate claims against the supplied evidence and identify unsupported or conflicting claims.",
        backstory=(
            "You are a fact verification specialist. "
            "You do not invent verification evidence. "
            "You assess claims only against the supplied research material."
        ),
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
