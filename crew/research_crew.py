import os
import time
import re

from crewai import Crew, Process

from agents.planner import create_planner
from agents.web_researcher import create_web_researcher
from agents.academic_researcher import create_academic_researcher
from agents.industry_researcher import create_industry_researcher
from agents.evidence_analyst import create_evidence_analyst
from agents.fact_checker import create_fact_checker
from agents.synthesizer import create_synthesizer

from tasks.research_tasks import create_tasks

from tools.web_search import web_search_tool
from tools.academic_search import academic_search_tool


class ResearchCrew:

    def __init__(self):

        self.agents = {
            "planner": create_planner(),
            "web_researcher": create_web_researcher(),
            "academic_researcher": create_academic_researcher(),
            "industry_researcher": create_industry_researcher(),
            "evidence_analyst": create_evidence_analyst(),
            "fact_checker": create_fact_checker(),
            "synthesizer": create_synthesizer(),
        }

    def get_result_limit(self, depth: str) -> int:

        return {
            "Quick": 2,
            "Standard": 3,
            "Deep": 4,
        }.get(depth, 3)

    def extract_wait_time(self, error_text: str) -> float:

        match = re.search(
            r"try again in ([0-9.]+)s",
            error_text.lower()
        )

        if match:
            return float(match.group(1)) + 2

        return 8

    def collect_web_evidence(
        self,
        question: str,
        limit: int
    ) -> str:

        os.environ["RESEARCH_MAX_RESULTS"] = str(limit)

        result = web_search_tool.run(
            question
        )

        return str(result)[:5000]

    def collect_academic_evidence(
        self,
        question: str,
        limit: int
    ) -> str:

        os.environ["RESEARCH_MAX_RESULTS"] = str(limit)

        result = academic_search_tool.run(
            question
        )

        return str(result)[:5000]

    def collect_industry_evidence(
        self,
        question: str,
        limit: int
    ) -> str:

        os.environ["RESEARCH_MAX_RESULTS"] = str(limit)

        industry_query = (
            f"{question} companies products "
            f"industry adoption implementation"
        )

        result = web_search_tool.run(
            industry_query
        )

        return str(result)[:5000]

    def run(
        self,
        question: str,
        depth: str = "Standard",
        max_results: int = 3
    ) -> str:

        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError(
                "GROQ_API_KEY is missing."
            )

        result_limit = self.get_result_limit(depth)

        # --------------------------------------------------
        # 1. Collect external evidence outside the LLM.
        # --------------------------------------------------

        web_evidence = self.collect_web_evidence(
            question,
            result_limit
        )

        academic_evidence = self.collect_academic_evidence(
            question,
            result_limit
        )

        industry_evidence = self.collect_industry_evidence(
            question,
            result_limit
        )

        # --------------------------------------------------
        # 2. Build LLM tasks with collected evidence.
        # --------------------------------------------------

        tasks = create_tasks(
            agents=self.agents,
            question=question,
            depth=depth,
            max_results=result_limit,
            web_evidence=web_evidence,
            academic_evidence=academic_evidence,
            industry_evidence=industry_evidence,
        )

        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
        )

        # --------------------------------------------------
        # 3. Run the seven-agent analysis pipeline.
        # --------------------------------------------------

        max_attempts = 3

        for attempt in range(max_attempts):

            try:

                result = crew.kickoff()

                if hasattr(result, "raw"):
                    return result.raw

                return str(result)

            except Exception as exc:

                error_text = str(exc)

                is_rate_limit = (
                    "ratelimit" in error_text.lower()
                    or "rate limit" in error_text.lower()
                    or "429" in error_text
                    or "tokens per minute" in error_text.lower()
                )

                if not is_rate_limit:
                    raise

                if attempt == max_attempts - 1:
                    raise RuntimeError(
                        "The research workflow could not be "
                        "completed because the Groq rate limit "
                        "was reached. Please wait and try again."
                    ) from exc

                time.sleep(
                    max(
                        self.extract_wait_time(error_text),
                        5
                    )
                )

        raise RuntimeError(
            "Research workflow could not be completed."
        )
