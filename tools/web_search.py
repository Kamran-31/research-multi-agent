import os

from crewai.tools import tool
from tavily import TavilyClient


def get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not configured.")

    return TavilyClient(api_key=api_key)


@tool("web_search")
def web_search_tool(query: str) -> str:
    """Search the web and return compact research evidence."""

    query = query.strip()

    if not query:
        return "No search query was provided."

    try:
        max_results = int(
            os.getenv("RESEARCH_MAX_RESULTS", "3")
        )

        client = get_tavily_client()

        response = client.search(
            query=query,
            search_depth="basic",
            max_results=max_results,
            include_answer=False,
            include_raw_content=False,
        )

        results = response.get("results", [])

        if not results:
            return "No web results were found."

        output = ["WEB EVIDENCE"]

        for index, result in enumerate(
            results,
            start=1,
        ):
            title = result.get(
                "title",
                "Untitled",
            )

            url = result.get(
                "url",
                "",
            )

            content = result.get(
                "content",
                "",
            )

            output.append(
                f"""
SOURCE {index}
Title: {title}
URL: {url}
Evidence:
{content[:900]}
"""
            )

        return "\n".join(output)

    except Exception as exc:
        return f"Web search failed: {exc}"
