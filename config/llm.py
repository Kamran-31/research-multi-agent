from functools import lru_cache

import crewai.llms.cache as _crewai_cache
from crewai import LLM

# Prevent CrewAI from sending unsupported cache-breakpoint
# metadata to Groq.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

MODEL_NAME = "openai/gpt-oss-120b"


@lru_cache(maxsize=10)
def get_llm(max_tokens: int = 700) -> LLM:
    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.6,
        max_tokens=max_tokens,
        reasoning_effort="low",
        timeout=120,
    )
