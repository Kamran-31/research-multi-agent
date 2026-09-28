import requests

from crewai.tools import tool


OPENALEX_URL = "https://api.openalex.org/works"


@tool("academic_search")
def academic_search_tool(query: str) -> str:
    """Search OpenAlex for scholarly works relevant to a research question."""

    query = query.strip()

    if not query:
        return "No academic search query was provided."

    response = requests.get(
        OPENALEX_URL,
        params={
            "search": query,
            "per-page": 8,
            "sort": "relevance_score:desc",
        },
        timeout=25,
        headers={
            "User-Agent": "ResearchIntelligence/1.0"
        },
    )

    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    if not results:
        return "No academic works were found."

    output = ["ACADEMIC SEARCH RESULTS"]

    for index, work in enumerate(results, start=1):
        title = (
            work.get("display_name")
            or work.get("title")
            or "Untitled"
        )

        primary_location = work.get("primary_location") or {}

        url = (
            primary_location.get("landing_page_url")
            or work.get("doi")
            or ""
        )

        abstract = reconstruct_abstract(
            work.get("abstract_inverted_index")
        )

        output.append(
            f"""
SOURCE {index}
Title: {title}
Year: {work.get("publication_year")}
URL: {url}
Citations: {work.get("cited_by_count", 0)}
Abstract:
{abstract[:3000]}
"""
        )

    return "\n".join(output)


def reconstruct_abstract(inverted_index) -> str:
    if not inverted_index:
        return "No abstract available."

    words = []

    for word, positions in inverted_index.items():
        for position in positions:
            words.append((position, word))

    words.sort(key=lambda item: item[0])

    return " ".join(word for _, word in words)
