import re


def clean_markdown(text: str) -> str:
    text = text.strip()

    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text,
    )

    return text


def extract_sources(text: str) -> list[dict]:
    sources = []
    seen = set()

    markdown_links = re.findall(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        text,
    )

    for title, url in markdown_links:
        if url not in seen:
            sources.append(
                {
                    "title": title,
                    "url": url,
                }
            )
            seen.add(url)

    if sources:
        return sources

    urls = re.findall(
        r"https?://[^\s<>)]+",
        text,
    )

    for url in urls:
        url = url.rstrip(".,;")

        if url not in seen:
            sources.append(
                {
                    "title": url,
                    "url": url,
                }
            )
            seen.add(url)

    return sources
