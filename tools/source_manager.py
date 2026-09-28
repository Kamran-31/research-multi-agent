from urllib.parse import urlsplit


def normalize_url(url: str) -> str:
    url = url.strip()

    if not url:
        return ""

    parts = urlsplit(url)

    if not parts.scheme or not parts.netloc:
        return url

    path = parts.path.rstrip("/")

    return (
        f"{parts.scheme.lower()}://"
        f"{parts.netloc.lower()}"
        f"{path}"
    )


def deduplicate_sources(sources: list[dict]) -> list[dict]:
    seen = set()
    unique = []

    for source in sources:
        url = normalize_url(source.get("url", ""))

        if not url or url in seen:
            continue

        seen.add(url)

        normalized = dict(source)
        normalized["url"] = url

        unique.append(normalized)

    return unique
