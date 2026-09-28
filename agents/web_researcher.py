from crewai import Agent
from config.llm import get_llm
from tools.web_search import web_search_tool
from tools.web_extract import extract_webpage_tool


def create_web_researcher() -> Agent:
    return Agent(
        role="Web Research Specialist",
        goal=(
            "Find concise, current and authoritative web evidence "
            "for the assigned research questions."
        ),
        backstory=(
            "You are an investigative web researcher. You prioritize official "
            "sources, primary sources, institutions and reputable reporting."
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
