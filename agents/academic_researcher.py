from crewai import Agent

from config.llm import get_llm
from tools.academic_search import academic_search_tool
from tools.web_extract import extract_webpage_tool


def create_academic_researcher() -> Agent:
    return Agent(
        role="Academic Research Specialist",
        goal=(
            "Find and interpret relevant scholarly literature, studies and "
            "technical research that support or challenge the research question."
        ),
        backstory=(
            "You are an academic research analyst experienced with scholarly "
            "literature. You distinguish research papers and institutional "
            "studies from ordinary web commentary."
        ),
        tools=[
            academic_search_tool,
            extract_webpage_tool,
        ],
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )
