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

    def get_limit(self, depth):

        return {
            "Quick": 2,
            "Standard": 2,
            "Deep": 3,
        }.get(depth, 2)

    def search_web(self, query, limit):

        os.environ["RESEARCH_MAX_RESULTS"] = str(limit)

        result = web_search_tool.run(query)

        return str(result)[:3500]

    def search_academic(self, query, limit):

        os.environ["RESEARCH_MAX_RESULTS"] = str(limit)

        result = academic_search_tool.run(query)

        return str(result)[:3000]

    def run(
        self,
        question,
        depth="Standard",
        max_results=2,
    ):

        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError("GROQ_API_KEY is missing.")

        limit = self.get_limit(depth)

        # -----------------------------------------
        # External research happens WITHOUT Groq.
        # -----------------------------------------

        web_evidence = self.search_web(
            question,
            limit,
        )

        academic_evidence = self.search_academic(
            question,
            limit,
        )

        industry_evidence = self.search_web(
            f"{question} companies products adoption implementation",
            limit,
        )

        # -----------------------------------------
        # Create compact agent tasks.
        # -----------------------------------------

        tasks = create_tasks(
            agents=self.agents,
            question=question,
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

        # -----------------------------------------
        # Run with a small number of retries.
        # -----------------------------------------

        for attempt in range(2):

            try:

                result = crew.kickoff()

                if hasattr(result, "raw"):
                    return result.raw

                return str(result)

            except Exception as exc:

                error = str(exc).lower()

                rate_limit = (
                    "rate limit" in error
                    or "ratelimit" in error
                    or "429" in error
                    or "tokens per minute" in error
                )

                if not rate_limit:
                    raise

                if attempt == 1:
                    raise RuntimeError(
                        "Groq's token-per-minute limit was reached. "
                        "Please wait approximately one minute and "
                        "run the research again."
                    ) from exc

                match = re.search(
                    r"try again in ([0-9.]+)s",
                    error,
                )

                wait = (
                    float(match.group(1)) + 3
                    if match
                    else 10
                )

                time.sleep(wait)

        raise RuntimeError(
            "Research workflow failed."
        )
