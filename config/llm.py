from functools import lru_cache

import crewai.llms.cache as _crewai_cache
from crewai import LLM


_crewai_cache.mark_cache_breakpoint = lambda msg: msg


MODEL_NAME = "openai/gpt-oss-120b"


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.2,
        max_tokens=600,
        reasoning_effort="low",
        timeout=120,
        max_retries=1,
    )


@lru_cache(maxsize=1)
def get_synthesis_llm() -> LLM:
    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.2,
        max_tokens=1200,
        reasoning_effort="low",
        timeout=120,
        max_retries=1,
    )
