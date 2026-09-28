from crewai import Task


def create_tasks(
    agents: dict,
    question: str,
    depth: str,
    max_results: int,
) -> list[Task]:

    planner = Task(
        description=f"""
Create a research plan for:

{question}

Research depth:
{depth}

Target search results:
{max_results}

Produce:

1. Central research objective
2. Four to seven focused subquestions
3. Evidence required for each subquestion
4. Preferred source types
5. Important terms, entities and comparisons to investigate

Do not answer the research question yet.
Create the investigation plan only.
""",
        expected_output=(
            "A structured research plan containing the objective, "
            "subquestions, evidence requirements and source priorities."
        ),
        agent=agents["planner"],
    )

    web = Task(
        description=f"""
Using the planner's research plan, conduct web research for:

{question}

Find current and authoritative web evidence.

Prioritize:
- official sources
- primary sources
- government or institutional sources
- reputable reporting
- recent documentation

For every important finding provide:

Claim:
Evidence:
Source:
URL:
Why it matters:

Do not fabricate sources.
""",
        expected_output=(
            "A source-grounded web research dossier containing claims, "
            "evidence and URLs."
        ),
        agent=agents["web_researcher"],
        context=[planner],
    )

    academic = Task(
        description=f"""
Using the planner's research plan, conduct academic research for:

{question}

Search scholarly literature and technical studies.

For important works provide:

Finding:
Paper title:
Publication year:
DOI or URL:
Why it matters:
Limitations:

Prefer relevant and recent literature while retaining foundational research where useful.
""",
        expected_output=(
            "An academic evidence dossier with bibliographic references "
            "and research findings."
        ),
        agent=agents["academic_researcher"],
        context=[planner],
    )

    industry = Task(
        description=f"""
Using the planner's research plan, conduct industry research for:

{question}

Investigate:
- companies
- products
- deployments
- market developments
- adoption
- practical implementations

Separate company claims from independently supported facts.

For each important finding provide:

Claim:
Evidence:
Organization/source:
URL:
Relevance:
""",
        expected_output=(
            "An industry evidence dossier with claims, evidence and URLs."
        ),
        agent=agents["industry_researcher"],
        context=[planner],
    )

    evidence = Task(
        description="""
Analyze the web, academic and industry research dossiers.

Create an evidence map.

For each major claim identify:

- Claim
- Supporting evidence
- Sources
- Source quality
- Agreement between sources
- Contradictions
- Evidence gaps

Do not introduce facts that were not found by the researchers.
""",
        expected_output=(
            "A structured evidence map containing claims, evidence, "
            "source quality, contradictions and gaps."
        ),
        agent=agents["evidence_analyst"],
        context=[web, academic, industry],
    )

    fact_check = Task(
        description="""
Fact-check the evidence map.

Focus particularly on:

- numerical claims
- dates
- company/product claims
- important conclusions
- conflicting evidence

Use web search and webpage extraction where appropriate.

For each checked claim report:

Claim:
Verification status:
Verification evidence:
Source URL:
Explanation:

Allowed statuses:

Confirmed
Partially supported
Conflicting
Unverified

Do not classify weak evidence as confirmed.
""",
        expected_output=(
            "A fact-check dossier with verification statuses and source URLs."
        ),
        agent=agents["fact_checker"],
        context=[evidence],
    )

    synthesis = Task(
        description=f"""
Write the final research report for:

{question}

Use only the evidence map and fact-check dossier.

Structure:

# Executive Summary

# Research Findings

# Evidence Analysis

# Contradictions and Uncertainty

# Practical Implications

# Conclusion

# Sources

Rules:

- Do not invent facts.
- Do not invent sources.
- Do not invent statistics.
- Do not invent quotations.
- Do not present unverified claims as facts.
- Attribute company claims.
- Preserve important disagreements.
- Clearly communicate uncertainty.
- Include source URLs.
""",
        expected_output=(
            "A polished, source-grounded research report with a complete "
            "Sources section."
        ),
        agent=agents["synthesizer"],
        context=[evidence, fact_check],
    )

    return [
        planner,
        web,
        academic,
        industry,
        evidence,
        fact_check,
        synthesis,
    ]
