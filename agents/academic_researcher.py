from crewai import Agent
from config.llm import get_llm
from tools.academic_search import academic_search_tool
from tools.web_extract import extract_webpage_tool


def create_academic_researcher() -> Agent:
    return Agent(
        role="Academic Research Specialist",
        goal=(
            "Find concise scholarly evidence relevant to the research question "
            "and identify important findings and limitations."
        ),
        backstory=(
            "You are an academic research analyst. You distinguish scholarly "
            "evidence from ordinary web commentary."
        ),
        tools=[
            academic_search_tool,
            extract_webpage_tool,
        ],
        llm=get_llm(),
        allow_delegation=False,
        max_iter=3,
        verbose=False,
    )
