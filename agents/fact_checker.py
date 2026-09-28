from crewai import Agent

from config.llm import get_llm
from tools.web_search import web_search_tool
from tools.web_extract import extract_webpage_tool


def create_fact_checker() -> Agent:
    return Agent(
        role="Research Fact Checker",
        goal=(
            "Challenge important claims, investigate contradictions and determine "
            "whether the evidence is sufficiently supported."
        ),
        backstory=(
            "You are a skeptical verification specialist. You cross-check "
            "important claims against reliable sources and explicitly identify "
            "uncertainty instead of accepting weak evidence."
        ),
        tools=[
            web_search_tool,
            extract_webpage_tool,
        ],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
