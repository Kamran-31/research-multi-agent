from crewai import Agent
from config.llm import get_llm
from tools.web_search import web_search_tool
from tools.web_extract import extract_webpage_tool


def create_fact_checker() -> Agent:
    return Agent(
        role="Research Fact Checker",
        goal=(
            "Verify the most important claims, especially numerical claims, "
            "dates, company claims and disputed findings."
        ),
        backstory=(
            "You are a skeptical verification specialist. You cross-check "
            "important claims and clearly identify uncertainty."
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
