from crewai import Task


def create_tasks(
    agents: dict,
    question: str,
    depth: str,
    max_results: int,
) -> list[Task]:

    planner = Task(
        description=f"""
Create a concise research plan for this question:

{question}

Research depth: {depth}

Identify:

1. The main research objective.
2. Four focused subquestions.
3. What evidence is needed.
4. Preferred source types.

Keep the plan concise.
Do not answer the question yet.
""",
        expected_output=(
            "A concise research plan with one objective, "
            "four subquestions and evidence requirements."
        ),
        agent=agents["planner"],
    )

    web = Task(
        description=f"""
Research this question using the planner's guidance:

{question}

Find current web evidence.

Prioritize:
- official sources
- government or institutional sources
- primary sources
- reputable reporting

Return ONLY the most useful findings.

For each finding provide:

Finding:
Evidence:
Source:
URL:

Maximum useful findings: {max_results}

Do not write a long report.
Do not invent sources.
""",
        expected_output=(
            "A concise web evidence dossier containing "
            "key findings and source URLs."
        ),
        agent=agents["web_researcher"],
        context=[planner],
    )

    academic = Task(
        description=f"""
Research this question using scholarly literature:

{question}

Find relevant academic evidence.

For each important work provide:

Finding:
Paper:
Year:
URL or DOI:
Limitation:

Return only the most relevant works.

Maximum works: {max_results}

Do not write a long literature review.
Do not invent papers.
""",
        expected_output=(
            "A concise academic evidence dossier with "
            "relevant papers, findings and URLs."
        ),
        agent=agents["academic_researcher"],
        context=[planner],
    )

    industry = Task(
        description=f"""
Investigate the industry side of this question:

{question}

Look for:

- companies
- products
- deployments
- adoption
- real-world implementations
- industry reports

For each important finding provide:

Finding:
Evidence:
Organization/source:
URL:

Maximum useful findings: {max_results}

Clearly distinguish company claims from independently supported evidence.
Keep the response concise.
""",
        expected_output=(
            "A concise industry evidence dossier "
            "with findings and source URLs."
        ),
        agent=agents["industry_researcher"],
        context=[planner],
    )

    evidence = Task(
        description="""
Analyze the three research dossiers.

Create a compact evidence map.

For each major claim identify:

Claim:
Supporting evidence:
Sources:
Agreement or contradiction:
Evidence strength:
Gap or limitation:

Do not introduce new facts.
Do not write a final report.
Keep the evidence map concise.
""",
        expected_output=(
            "A compact evidence map containing major claims, "
            "supporting sources, contradictions and gaps."
        ),
        agent=agents["evidence_analyst"],
        context=[web, academic, industry],
    )

    fact_check = Task(
        description="""
Fact-check the most important claims in the evidence map.

Prioritize:

- statistics
- numerical claims
- dates
- company/product claims
- controversial findings

Use web research only where verification is necessary.

For each checked claim provide:

Claim:
Status:
Evidence:
Source URL:

Use only:

Confirmed
Partially supported
Conflicting
Unverified

Keep the fact-check concise.
""",
        expected_output=(
            "A concise fact-check dossier with verification "
            "statuses and source URLs."
        ),
        agent=agents["fact_checker"],
        context=[evidence],
    )

    synthesis = Task(
        description=f"""
Write the final research report for:

{question}

Use only the evidence map and fact-check results.

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
- Do not present unverified claims as facts.
- Attribute company claims.
- Preserve important contradictions.
- Include source URLs.

Keep the report informative but concise.
""",
        expected_output=(
            "A concise, polished research report with "
            "source URLs and clearly stated uncertainty."
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
