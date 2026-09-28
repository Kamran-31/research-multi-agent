import os

from crewai.tools import tool
from tavily import TavilyClient


def get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")

    if api_key:
        return TavilyClient(api_key=api_key)

    return TavilyClient()


@tool("web_search")
def web_search_tool(query: str) -> str:
    """Search the web and return relevant titles, URLs and evidence snippets."""

    query = query.strip()

    if not query:
        return "No search query was provided."

    client = get_tavily_client()

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=6,
        include_answer=False,
        include_raw_content=False,
    )

    results = response.get("results", [])

    if not results:
        return "No web results were found."

    output = ["WEB SEARCH RESULTS"]

    for index, result in enumerate(results, start=1):
        output.append(
            f"""
SOURCE {index}
Title: {result.get("title", "Untitled")}
URL: {result.get("url", "")}
Evidence:
{result.get("content", "")}
"""
        )

    return "\n".join(output)
