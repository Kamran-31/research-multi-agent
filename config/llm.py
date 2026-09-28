from functools import lru_cache

import crewai.llms.cache as _crewai_cache
from crewai import LLM

# CrewAI's cache breakpoint is not supported by the current Groq request format.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

MODEL_NAME = "openai/gpt-oss-120b"


@lru_cache(maxsize=10)
def get_llm(max_tokens: int = 700) -> LLM:
    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.1,
        max_tokens=max_tokens,
    )
