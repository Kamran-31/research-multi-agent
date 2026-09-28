from crewai import Agent
from config.llm import get_llm
from tools.web_search import web_search_tool


def create_industry_researcher() -> Agent:
    return Agent(
        role="Industry Research Specialist",
        goal="Identify concise evidence about real-world industry adoption.",
        backstory=(
            "You investigate companies, products, deployments, "
            "market activity and practical implementations."
        ),
        tools=[web_search_tool],
        llm=get_llm(650),
        allow_delegation=False,
        max_iter=2,
        verbose=False,
    )
