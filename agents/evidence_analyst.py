from crewai import Agent

from config.llm import get_llm


def create_evidence_analyst() -> Agent:
    return Agent(
        role="Evidence Analysis Specialist",
        goal=(
            "Convert raw research into an organized evidence map containing "
            "claims, supporting evidence, source quality, contradictions and gaps."
        ),
        backstory=(
            "You are a meticulous evidence analyst. You compare claims across "
            "researchers, identify duplicated evidence, distinguish observations "
            "from conclusions and flag unsupported assertions."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
