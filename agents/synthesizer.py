from crewai import Agent

from config.llm import get_llm


def create_synthesizer() -> Agent:
    return Agent(
        role="Senior Research Report Synthesizer",
        goal=(
            "Produce a clear, balanced and source-grounded final research report "
            "from the verified evidence supplied by the research team."
        ),
        backstory=(
            "You are a senior research writer. You synthesize evidence without "
            "inventing facts, distinguish strong evidence from uncertainty, "
            "preserve contradictions and make source attribution clear."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
