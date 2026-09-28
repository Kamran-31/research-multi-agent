from functools import lru_cache

import crewai.llms.cache as _crewai_cache
from crewai import LLM


# CrewAI may add cache_breakpoint to messages.
# Groq does not accept this field.
_crewai_cache.mark_cache_breakpoint = lambda msg: msg


MODEL_NAME = "openai/gpt-oss-120b"


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.1,
        max_tokens=1000,
    )
