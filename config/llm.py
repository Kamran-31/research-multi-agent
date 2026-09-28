from functools import lru_cache

import crewai.llms.cache as _crewai_cache
from crewai import LLM


# Prevent CrewAI from sending cache_breakpoint to Groq.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

MODEL_NAME = "openai/gpt-oss-120b"


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.1,
        max_tokens=2048,
    )
