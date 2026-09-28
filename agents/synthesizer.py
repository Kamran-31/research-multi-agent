from crewai import Agent
from config.llm import get_llm


def create_synthesizer() -> Agent:
    return Agent(
        role="Senior Research Report Synthesizer",
        goal=(
            "Produce a clear, concise and source-grounded research report "
            "using only the verified evidence provided."
        ),
        backstory=(
            "You are a senior research writer. You synthesize evidence, "
            "preserve uncertainty and never invent facts or sources."
        ),
        llm=get_llm(),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
