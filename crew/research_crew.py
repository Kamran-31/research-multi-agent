import os
import time
from typing import Any

from crewai import Agent, Crew, Process

from config.llm import get_llm

from tasks.research_tasks import (
    planner_task,
    web_research_task,
    academic_research_task,
    industry_research_task,
    evidence_analysis_task,
    fact_check_task,
    synthesis_task,
)

from tools.web_search import web_search_tool
from tools.academic_search import academic_search_tool


# ---------------------------------------------------------
# Context limits
# ---------------------------------------------------------

MAX_PLAN_CHARS = 2200
MAX_EVIDENCE_CHARS = 3500
MAX_AGENT_OUTPUT_CHARS = 2800
MAX_EVIDENCE_MAP_CHARS = 3500
MAX_FACT_CHECK_CHARS = 3000


# ---------------------------------------------------------
# Groq rolling TPM protection
# ---------------------------------------------------------

AGENT_DELAY_SECONDS = 9


class ResearchCrew:

    def __init__(self):
        self.llm = get_llm()

        self.agents = self._create_agents()

    # -----------------------------------------------------
    # Seven REAL agents
    # -----------------------------------------------------

    def _create_agents(self):

        planner = Agent(
            role="Research Planner",
            goal="Decompose the research question into a precise research plan.",
            backstory=(
                "You are a research planning specialist who defines "
                "what must be investigated before research begins."
            ),
            llm=self.llm,
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

        web_researcher = Agent(
            role="Web Researcher",
            goal="Analyze current web evidence relevant to the research plan.",
            backstory=(
                "You specialize in current web evidence, official sources, "
                "institutions and reputable reporting."
            ),
            llm=self.llm,
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

        academic_researcher = Agent(
            role="Academic Researcher",
            goal="Analyze scholarly evidence relevant to the research question.",
            backstory=(
                "You specialize in academic literature, empirical findings "
                "and scholarly limitations."
            ),
            llm=self.llm,
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

        industry_researcher = Agent(
            role="Industry Researcher",
            goal="Analyze industry evidence, companies, products and adoption.",
            backstory=(
                "You specialize in real-world implementations, companies, "
                "products, deployments and industry trends."
            ),
            llm=self.llm,
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

        evidence_analyst = Agent(
            role="Evidence Analyst",
            goal="Cross-analyze research findings and identify strongest evidence.",
            backstory=(
                "You compare independent evidence streams, detect agreement, "
                "contradictions and research gaps."
            ),
            llm=self.llm,
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

        fact_checker = Agent(
            role="Fact Checker",
            goal="Verify the most important claims identified by the evidence analyst.",
            backstory=(
                "You specialize in detecting unsupported, conflicting and "
                "partially supported research claims."
            ),
            llm=self.llm,
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

        synthesizer = Agent(
            role="Research Synthesizer",
            goal="Transform verified research into one coherent final report.",
            backstory=(
                "You are a senior research analyst who synthesizes "
                "multi-source evidence into precise reports."
            ),
            llm=self.llm,
            allow_delegation=False,
            max_iter=1,
            verbose=False,
        )

        return {
            "planner": planner,
            "web_researcher": web_researcher,
            "academic_researcher": academic_researcher,
            "industry_researcher": industry_researcher,
            "evidence_analyst": evidence_analyst,
            "fact_checker": fact_checker,
            "synthesizer": synthesizer,
        }

    # -----------------------------------------------------
    # Utility
    # -----------------------------------------------------

    @staticmethod
    def _clean(value: Any, limit: int) -> str:
        if value is None:
            return ""

        text = str(value).strip()

        if len(text) <= limit:
            return text

        return text[:limit] + "\n...[context truncated]"

    # -----------------------------------------------------
    # Execute ONE agent
    # -----------------------------------------------------

    def _run_agent(self, agent, task):
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()

        output = getattr(result, "raw", None)

        if output is None:
            output = str(result)

        output = str(output).strip()

        if not output:
            raise RuntimeError(
                f"{agent.role} returned an empty response."
            )

        return output

    # -----------------------------------------------------
    # External research retrieval
    # -----------------------------------------------------

    def _get_web_evidence(
        self,
        question: str,
        plan: str,
        max_results: int,
    ) -> str:

        query = (
            f"{question} "
            f"Key research areas: {plan[:1000]}"
        )

        os.environ["RESEARCH_MAX_RESULTS"] = str(
            max(2, min(max_results, 3))
        )

        return self._clean(
            web_search_tool.run(query),
            MAX_EVIDENCE_CHARS,
        )

    def _get_academic_evidence(
        self,
        question: str,
        plan: str,
        max_results: int,
    ) -> str:

        query = (
            f"{question} "
            f"Research areas: {plan[:1000]}"
        )

        os.environ["RESEARCH_MAX_RESULTS"] = str(
            max(2, min(max_results, 3))
        )

        return self._clean(
            academic_search_tool.run(query),
            MAX_EVIDENCE_CHARS,
        )

    def _get_industry_evidence(
        self,
        question: str,
        plan: str,
        max_results: int,
    ) -> str:

        query = (
            f"{question} "
            f"Companies products adoption implementation: "
            f"{plan[:1000]}"
        )

        os.environ["RESEARCH_MAX_RESULTS"] = str(
            max(2, min(max_results, 3))
        )

        return self._clean(
            web_search_tool.run(query),
            MAX_EVIDENCE_CHARS,
        )

    # -----------------------------------------------------
    # MAIN COLLABORATIVE RESEARCH PIPELINE
    # -----------------------------------------------------

    def run(
        self,
        question: str,
        depth: str = "standard",
        max_results: int = 3,
        status_callback=None,
    ) -> str:

        question = question.strip()

        if not question:
            raise ValueError("Research question cannot be empty.")

        def status(message):
            if status_callback:
                status_callback(message)

        # =================================================
        # AGENT 1 — PLANNER
        # =================================================

        status("Agent 1/7 — Research Planner is analyzing the question...")

        planner = self.agents["planner"]

        task = planner_task(
            planner,
            question,
            depth,
        )

        plan = self._run_agent(planner, task)

        plan = self._clean(
            plan,
            MAX_PLAN_CHARS,
        )

        time.sleep(AGENT_DELAY_SECONDS)

        # =================================================
        # EXTERNAL RESEARCH COLLECTION
        #
        # These are API calls, not additional Groq calls.
        # =================================================

        status("Collecting web evidence...")

        web_evidence = self._get_web_evidence(
            question,
            plan,
            max_results,
        )

        status("Collecting academic evidence...")

        academic_evidence = self._get_academic_evidence(
            question,
            plan,
            max_results,
        )

        status("Collecting industry evidence...")

        industry_evidence = self._get_industry_evidence(
            question,
            plan,
            max_results,
        )

        # =================================================
        # AGENT 2 — WEB
        # =================================================

        status("Agent 2/7 — Web Researcher is analyzing evidence...")

        web_agent = self.agents["web_researcher"]

        task = web_research_task(
            web_agent,
            question,
            plan,
            web_evidence,
        )

        web_findings = self._run_agent(
            web_agent,
            task,
        )

        web_findings = self._clean(
            web_findings,
            MAX_AGENT_OUTPUT_CHARS,
        )

        time.sleep(AGENT_DELAY_SECONDS)

        # =================================================
        # AGENT 3 — ACADEMIC
        # =================================================

        status("Agent 3/7 — Academic Researcher is analyzing evidence...")

        academic_agent = self.agents["academic_researcher"]

        task = academic_research_task(
            academic_agent,
            question,
            plan,
            academic_evidence,
        )

        academic_findings = self._run_agent(
            academic_agent,
            task,
        )

        academic_findings = self._clean(
            academic_findings,
            MAX_AGENT_OUTPUT_CHARS,
        )

        time.sleep(AGENT_DELAY_SECONDS)

        # =================================================
        # AGENT 4 — INDUSTRY
        # =================================================

        status("Agent 4/7 — Industry Researcher is analyzing evidence...")

        industry_agent = self.agents["industry_researcher"]

        task = industry_research_task(
            industry_agent,
            question,
            plan,
            industry_evidence,
        )

        industry_findings = self._run_agent(
            industry_agent,
            task,
        )

        industry_findings = self._clean(
            industry_findings,
            MAX_AGENT_OUTPUT_CHARS,
        )

        time.sleep(AGENT_DELAY_SECONDS)

        # =================================================
        # AGENT 5 — EVIDENCE ANALYST
        # =================================================

        status("Agent 5/7 — Evidence Analyst is cross-checking findings...")

        evidence_agent = self.agents["evidence_analyst"]

        task = evidence_analysis_task(
            evidence_agent,
            question,
            plan,
            web_findings,
            academic_findings,
            industry_findings,
        )

        evidence_map = self._run_agent(
            evidence_agent,
            task,
        )

        evidence_map = self._clean(
            evidence_map,
            MAX_EVIDENCE_MAP_CHARS,
        )

        time.sleep(AGENT_DELAY_SECONDS)

        # =================================================
        # AGENT 6 — FACT CHECKER
        # =================================================

        status("Agent 6/7 — Fact Checker is verifying key claims...")

        fact_agent = self.agents["fact_checker"]

        task = fact_check_task(
            fact_agent,
            question,
            evidence_map,
        )

        fact_check = self._run_agent(
            fact_agent,
            task,
        )

        fact_check = self._clean(
            fact_check,
            MAX_FACT_CHECK_CHARS,
        )

        time.sleep(AGENT_DELAY_SECONDS)

        # =================================================
        # AGENT 7 — SYNTHESIZER
        # =================================================

        status("Agent 7/7 — Research Synthesizer is generating the report...")

        synthesizer = self.agents["synthesizer"]

        task = synthesis_task(
            synthesizer,
            question,
            plan,
            evidence_map,
            fact_check,
        )

        final_report = self._run_agent(
            synthesizer,
            task,
        )

        status("Research completed — all 7 agents participated.")

        return final_report
