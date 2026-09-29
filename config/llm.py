from functools import lru_cache

import crewai.llms.cache as _crewai_cache
from crewai import LLM


# ---------------------------------------------------------
# Groq GPT-OSS compatibility
# Prevent CrewAI from injecting cache_breakpoint into
# the Groq request, which GPT-OSS rejects in this setup.
# ---------------------------------------------------------
_crewai_cache.mark_cache_breakpoint = lambda msg: msg


MODEL_NAME = "openai/gpt-oss-120b"


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    return LLM(
        model=f"groq/{MODEL_NAME}",
        temperature=0.2,

        # Keep every individual completion bounded.
        max_tokens=1200,

        # GPT-OSS supports low reasoning effort.
        reasoning_effort="low",

        timeout=120,
        max_retries=1,
    )
