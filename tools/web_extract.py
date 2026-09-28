import os

from crewai.tools import tool
from tavily import TavilyClient


def get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")

    if api_key:
        return TavilyClient(api_key=api_key)

    return TavilyClient()


@tool("extract_webpage")
def extract_webpage_tool(url: str) -> str:
    """Extract readable content from a specific webpage URL."""

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        return "Invalid URL. Provide a complete http or https URL."

    client = get_tavily_client()

    response = client.extract(
        urls=[url],
        extract_depth="basic",
        format="markdown",
    )

    results = response.get("results", [])

    if not results:
        return f"No content could be extracted from {url}."

    content = results[0].get("raw_content", "")

    return (
        f"SOURCE URL:\n{url}\n\n"
        f"EXTRACTED CONTENT:\n{content[:15000]}"
    )
