import os
import re
import time

from crewai import Crew, Process

from agents.planner import create_planner
from agents.web_researcher import create_web_researcher
from agents.academic_researcher import create_academic_researcher
from agents.industry_researcher import create_industry_researcher
from agents.evidence_analyst import create_evidence_analyst
from agents.fact_checker import create_fact_checker
from agents.synthesizer import create_synthesizer

from tasks.research_tasks import create_tasks


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

        limits = {
            "Quick": 2,
            "Standard": 3,
            "Deep": 4,
        }

        return limits.get(depth, 3)

    def extract_wait_time(self, error_text: str) -> float:

        patterns = [
            r"try again in ([0-9.]+)s",
            r"retry.after.*?([0-9.]+)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                error_text.lower()
            )

            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    pass

        return 8.0

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

        os.environ["RESEARCH_MAX_RESULTS"] = str(
            result_limit
        )

        tasks = create_tasks(
            agents=self.agents,
            question=question,
            depth=depth,
            max_results=result_limit,
        )

        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
        )

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
                        "The research workflow exceeded the "
                        "current Groq token-per-minute limit. "
                        "Please wait about one minute and try again."
                    ) from exc

                wait_time = self.extract_wait_time(
                    error_text
                )

                # Add a small safety buffer.
                wait_time = max(
                    wait_time + 2,
                    5
                )

                time.sleep(wait_time)

        raise RuntimeError(
            "Research workflow could not be completed."
        )
