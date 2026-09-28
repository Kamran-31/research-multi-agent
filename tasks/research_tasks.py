from crewai import Task


def create_tasks(
    agents: dict,
    question: str,
    depth: str,
    max_results: int,
    web_evidence: str = "",
    academic_evidence: str = "",
    industry_evidence: str = "",
) -> list[Task]:

    planner = Task(
        description=f"""
Create a compact research plan for:

{question}

Research depth: {depth}

Return:

Objective:
Subquestions:
- ...
- ...
- ...
- ...

Evidence needed:

Maximum 150 words.
""",
        expected_output="A concise research plan.",
        agent=agents["planner"],
    )

    web = Task(
        description=f"""
Analyze the following web research collected for this question:

QUESTION:
{question}

WEB EVIDENCE:
{web_evidence}

Identify the most relevant findings.

For each finding:

Finding:
Evidence:
Source:
URL:

Maximum {max_results} findings.
Maximum 300 words.

Do not search the web.
Do not invent information.
""",
        expected_output="A concise web evidence dossier.",
        agent=agents["web_researcher"],
        context=[planner],
    )

    academic = Task(
        description=f"""
Analyze the following academic research collected for this question:

QUESTION:
{question}

ACADEMIC EVIDENCE:
{academic_evidence}

Identify the most relevant scholarly findings.

For each:

Finding:
Paper:
Year:
URL/DOI:
Limitation:

Maximum {max_results} works.
Maximum 300 words.

Do not search the web.
Do not invent papers.
""",
        expected_output="A concise academic evidence dossier.",
        agent=agents["academic_researcher"],
        context=[planner],
    )

    industry = Task(
        description=f"""
Analyze the following industry research collected for this question:

QUESTION:
{question}

INDUSTRY EVIDENCE:
{industry_evidence}

Identify the most relevant findings.

For each:

Finding:
Evidence:
Organization:
URL:

Maximum {max_results} findings.
Maximum 300 words.

Clearly distinguish company claims from independent evidence.

Do not search the web.
Do not invent information.
""",
        expected_output="A concise industry evidence dossier.",
        agent=agents["industry_researcher"],
        context=[planner],
    )

    evidence = Task(
        description="""
Analyze the three research dossiers.

Create a compact evidence map.

For each major claim:

Claim:
Supporting Evidence:
Sources:
Agreement/Conflict:
Evidence Strength:
Gap:

Maximum 5 major claims.
Maximum 450 words.

Do not introduce outside information.
""",
        expected_output="A compact evidence map.",
        agent=agents["evidence_analyst"],
        context=[web, academic, industry],
    )

    fact_check = Task(
        description="""
Evaluate the important claims in the evidence map against the
research dossiers supplied earlier.

For each important claim:

Claim:
Status:
Supporting Evidence:
Source:

Status must be one of:

Confirmed
Partially supported
Conflicting
Unverified

Maximum 5 checks.
Maximum 400 words.

Do not perform external searches.
Do not invent verification evidence.
""",
        expected_output="A concise fact-check dossier.",
        agent=agents["fact_checker"],
        context=[web, academic, industry, evidence],
    )

    synthesis = Task(
        description=f"""
Write the final research report for:

{question}

Use ONLY the supplied evidence map and fact-check results.

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
- Preserve contradictions.
- Clearly identify unverified claims.
- Include source URLs.
- Maximum 800 words.
""",
        expected_output="A concise evidence-based research report.",
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
