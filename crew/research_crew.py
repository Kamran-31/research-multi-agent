import os
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
            "Deep": 5,
        }

        return limits.get(depth, 3)

    def run(
        self,
        question: str,
        depth: str = "Standard",
        max_results: int = 3,
    ) -> str:

        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError(
                "GROQ_API_KEY is missing."
            )

        result_limit = self.get_result_limit(depth)

        # Make the limit available to the search tools.
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

        last_error = None

        # One controlled retry for a temporary Groq rate limit.
        for attempt in range(2):

            try:

                result = crew.kickoff()

                if hasattr(result, "raw"):
                    return result.raw

                return str(result)

            except Exception as exc:

                last_error = exc

                error_text = str(exc).lower()

                if (
                    "ratelimit" not in error_text
                    and "rate limit" not in error_text
                    and "429" not in error_text
                ):
                    raise

                if attempt == 0:
                    time.sleep(7)
                else:
                    raise last_error

        raise last_error
