from crewai import Agent
from config.llm import get_llm
from tools.web_search import web_search_tool
from tools.web_extract import extract_webpage_tool


def create_industry_researcher() -> Agent:
    return Agent(
        role="Industry Research Specialist",
        goal=(
            "Find concise evidence about companies, products, deployments, "
            "adoption and real-world industry developments."
        ),
        backstory=(
            "You are an industry intelligence analyst. You separate company "
            "claims from independently supported evidence."
        ),
        tools=[
            web_search_tool,
            extract_webpage_tool,
        ],
        llm=get_llm(),
        allow_delegation=False,
        max_iter=3,
        verbose=False,
    )
