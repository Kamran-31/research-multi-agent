import os

from crewai import Agent, Crew, Process, Task

from config.llm import get_llm
from tools.web_search import web_search_tool
from tools.academic_search import academic_search_tool


class ResearchCrew:

    def __init__(self):

        self.agent = Agent(
            role="Research Intelligence Analyst",
            goal=(
                "Analyze multi-source research evidence and produce "
                "a concise, accurate, evidence-based research report."
            ),
            backstory=(
                "You are a senior research intelligence analyst. "
                "You evaluate web, academic and industry evidence, "
                "identify important findings, contradictions and "
                "uncertainties, then produce a professional report."
            ),
            llm=get_llm(),
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

    def get_limit(self, depth):

        return {
            "Quick": 2,
            "Standard": 3,
            "Deep": 4,
        }.get(depth, 2)

    def run(
        self,
        question: str,
        depth: str = "Quick",
        max_results: int = 2,
    ) -> str:

        limit = self.get_limit(depth)

        os.environ["RESEARCH_MAX_RESULTS"] = str(limit)

        # -------------------------------
        # External research
        # -------------------------------

        web = str(
            web_search_tool.run(question)
        )[:3500]

        academic = str(
            academic_search_tool.run(question)
        )[:3000]

        industry_query = (
            f"{question} companies products "
            f"industry adoption implementation"
        )

        industry = str(
            web_search_tool.run(industry_query)
        )[:3000]

        # -------------------------------
        # ONE LLM CALL
        # -------------------------------

        task = Task(
            description=f"""
You are producing a research intelligence report.

RESEARCH QUESTION:
{question}

RESEARCH DEPTH:
{depth}

WEB EVIDENCE:
{web}

ACADEMIC EVIDENCE:
{academic}

INDUSTRY EVIDENCE:
{industry}

Analyze the evidence and produce:

# Executive Summary

# Key Findings

# Evidence Analysis

# Risks and Uncertainty

# Practical Implications

# Conclusion

# Sources

Rules:

1. Use ONLY the supplied evidence.
2. Do not invent facts.
3. Do not invent statistics.
4. Do not invent sources.
5. Distinguish company claims from independent evidence.
6. Mention contradictions when present.
7. Clearly identify uncertainty.
8. Include source URLs.
9. Keep the report concise.
10. Maximum approximately 700 words.
""",
            expected_output=(
                "A concise evidence-based research report "
                "with source URLs."
            ),
            agent=self.agent,
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()

        if hasattr(result, "raw"):
            output = result.raw
        else:
            output = str(result)

        if not output or not output.strip():
            raise RuntimeError(
                "The research model returned an empty response."
            )

        return output
