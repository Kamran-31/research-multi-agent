from crewai import Task


def create_tasks(
    agents: dict,
    question: str,
    depth: str,
    max_results: int
) -> list[Task]:

    planner = Task(
        description=f"""
Create a compact research plan for:

{question}

Research depth: {depth}

Return ONLY:

Objective:
Subquestions:
- ...
- ...
- ...
- ...

Evidence needed:
- ...

Maximum 4 subquestions.
Maximum 180 words.
""",
        expected_output="A compact research plan under 180 words.",
        agent=agents["planner"],
    )

    web = Task(
        description=f"""
Research this question:

{question}

Use the research plan.

Search for reliable current web evidence.

Return at most {max_results} important findings.

For each finding use:

Finding:
Evidence:
Source:
URL:

Rules:
- Prefer official and primary sources.
- Do not write an essay.
- Do not repeat the question.
- Do not invent sources.
- Maximum 350 words.
""",
        expected_output="A compact web evidence dossier under 350 words.",
        agent=agents["web_researcher"],
        context=[planner],
    )

    academic = Task(
        description=f"""
Research this question using scholarly literature:

{question}

Use the research plan.

Return at most {max_results} relevant academic works.

For each:

Finding:
Paper:
Year:
URL/DOI:
Limitation:

Rules:
- Prefer relevant scholarly evidence.
- Do not write a literature review.
- Do not invent papers.
- Maximum 350 words.
""",
        expected_output="A compact academic evidence dossier under 350 words.",
        agent=agents["academic_researcher"],
        context=[planner],
    )

    industry = Task(
        description=f"""
Investigate the industry side of:

{question}

Use the research plan.

Find evidence involving:
- companies
- products
- deployments
- adoption
- real-world implementations

Return at most {max_results} important findings.

For each:

Finding:
Evidence:
Organization:
URL:

Rules:
- Clearly identify company claims.
- Do not write an industry essay.
- Do not invent sources.
- Maximum 350 words.
""",
        expected_output="A compact industry evidence dossier under 350 words.",
        agent=agents["industry_researcher"],
        context=[planner],
    )

    evidence = Task(
        description="""
Analyze the supplied web, academic and industry research.

Create a compact evidence map.

Return ONLY:

CLAIM 1
Claim:
Supporting Evidence:
Sources:
Agreement/Conflict:
Strength:
Gap:

CLAIM 2
...

Maximum 5 major claims.
Maximum 500 words.

Do not introduce outside information.
Do not write the final report.
""",
        expected_output="A compact evidence map containing no more than five major claims.",
        agent=agents["evidence_analyst"],
        context=[web, academic, industry],
    )

    fact_check = Task(
        description="""
Fact-check the evidence map.

Focus ONLY on the most important claims.

Prioritize:
- statistics
- dates
- major numerical claims
- company/product claims
- potentially conflicting claims

Verify only where necessary.

Return at most 5 checks:

Claim:
Status:
Evidence:
Source URL:

Status must be one of:
Confirmed
Partially supported
Conflicting
Unverified

Maximum 450 words.
""",
        expected_output="A compact fact-check containing no more than five verified claims.",
        agent=agents["fact_checker"],
        context=[evidence],
    )

    synthesis = Task(
        description=f"""
Write the final research report for:

{question}

Use ONLY:
1. The evidence map.
2. The fact-check results.

Structure:

# Executive Summary

# Key Findings

# Evidence Analysis

# Risks and Uncertainty

# Practical Implications

# Conclusion

# Sources

Rules:

- Do not invent facts.
- Do not invent statistics.
- Do not invent sources.
- Do not invent quotations.
- Clearly identify unverified claims.
- Preserve important contradictions.
- Include source URLs.
- Keep the report concise.
- Maximum approximately 900 words.
""",
        expected_output=(
            "A concise evidence-based research report with "
            "clear uncertainty and source URLs."
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
