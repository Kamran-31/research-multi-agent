import os

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

    def run(
        self,
        question: str,
        depth: str = "Standard",
        max_results: int = 5,
    ) -> str:

        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError(
                "GROQ_API_KEY is missing."
            )

        tasks = create_tasks(
            agents=self.agents,
            question=question,
            depth=depth,
            max_results=max_results,
        )

        crew = Crew(
            agents=list(self.agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()

        if hasattr(result, "raw"):
            return result.raw

        return str(result)
