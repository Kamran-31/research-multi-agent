from crewai import Agent

from config.llm import get_llm
from tools.web_search import web_search_tool
from tools.web_extract import extract_webpage_tool


def create_industry_researcher() -> Agent:
    return Agent(
        role="Industry and Market Research Specialist",
        goal=(
            "Investigate real-world industry activity, companies, products, "
            "market developments, technology adoption and practical deployments."
        ),
        backstory=(
            "You are an industry intelligence analyst. You investigate companies, "
            "products, deployments and market developments while separating "
            "company claims from independently supported evidence."
        ),
        tools=[
            web_search_tool,
            extract_webpage_tool,
        ],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
