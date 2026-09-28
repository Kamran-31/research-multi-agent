from crewai import Agent
from config.llm import get_llm


def create_industry_researcher() -> Agent:
    return Agent(
        role="Industry Research Specialist",
        goal="Analyze supplied industry evidence and extract important real-world findings.",
        backstory=(
            "You investigate companies, products, deployments and adoption "
            "using supplied evidence."
        ),
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=1,
        verbose=False,
    )
