from crewai import Task


def create_tasks(
    agents,
    question,
    web_evidence,
    academic_evidence,
    industry_evidence,
):

    planner = Task(
        description=f"""
Research question:

{question}

Create a research plan.

Return:
Objective:
Subquestions:
1.
2.
3.
4.

Maximum 120 words.
""",
        expected_output="Compact research plan.",
        agent=agents["planner"],
    )

    web = Task(
        description=f"""
Question:
{question}

Web evidence collected externally:

{web_evidence}

Extract only the 3 most important findings.

For each:
Finding:
Source:
URL:

Maximum 220 words.
Do not search for anything.
""",
        expected_output="Three concise web findings.",
        agent=agents["web_researcher"],
        context=[planner],
    )

    academic = Task(
        description=f"""
Question:
{question}

Academic evidence collected externally:

{academic_evidence}

Extract only the 3 most important findings.

For each:
Finding:
Paper:
Year:
URL:

Maximum 220 words.
Do not search for anything.
""",
        expected_output="Three concise academic findings.",
        agent=agents["academic_researcher"],
        context=[planner],
    )

    industry = Task(
        description=f"""
Question:
{question}

Industry evidence collected externally:

{industry_evidence}

Extract only the 3 most important findings.

For each:
Finding:
Organization:
Evidence:
URL:

Maximum 220 words.
Do not search for anything.
""",
        expected_output="Three concise industry findings.",
        agent=agents["industry_researcher"],
        context=[planner],
    )

    evidence = Task(
        description="""
Compare the research findings.

Identify the 4 most important claims.

For each:

Claim:
Evidence:
Sources:
Status:
Gap:

Maximum 350 words.
Use ONLY supplied evidence.
""",
        expected_output="Compact evidence map.",
        agent=agents["evidence_analyst"],
        context=[web, academic, industry],
    )

    fact_check = Task(
        description="""
Check the evidence map against the supplied research findings.

Return:

Claim:
Status:
Reason:
Source:

Use only:
Confirmed
Partially supported
Conflicting
Unverified

Maximum 300 words.
Do not perform external searches.
""",
        expected_output="Compact fact-check.",
        agent=agents["fact_checker"],
        context=[web, academic, industry, evidence],
    )

    synthesis = Task(
        description=f"""
Write the final research report.

Question:
{question}

Use only the evidence map and fact-check.

Structure:

# Executive Summary
# Key Findings
# Evidence Analysis
# Risks and Uncertainty
# Practical Implications
# Conclusion
# Sources

Do not invent facts.
Do not invent statistics.
Do not invent sources.

Maximum 700 words.
""",
        expected_output="Final research report.",
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
