from crewai import Task


def create_task(
    agent,
    description: str,
    expected_output: str,
) -> Task:
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )


def planner_task(agent, question: str, depth: str) -> Task:
    return create_task(
        agent=agent,
        description=f"""
You are the research planning specialist.

Research question:
{question}

Research depth:
{depth}

Create a compact research plan.

Identify:
1. Main research objective
2. Key subquestions
3. Evidence required
4. Relevant source categories

Do not research the answer.
Do not write a report.

Keep the plan concise.
""",
        expected_output="""
A compact research plan containing:
- objective
- key subquestions
- evidence requirements
- source categories
""",
    )


def web_research_task(
    agent,
    question: str,
    plan: str,
    web_evidence: str,
) -> Task:
    return create_task(
        agent=agent,
        description=f"""
You are the Web Research Specialist.

Research question:
{question}

Research plan:
{plan}

The external web-search system retrieved the following evidence:

{web_evidence}

Analyze the evidence according to the research plan.

Identify only the most relevant findings.

For each important finding provide:
- Claim
- Supporting evidence
- Source
- URL

Do not invent information.
Do not create a final report.
Do not repeat irrelevant evidence.

Be concise.
""",
        expected_output="""
A compact web research dossier containing the strongest
web-supported findings and source URLs.
""",
    )


def academic_research_task(
    agent,
    question: str,
    plan: str,
    academic_evidence: str,
) -> Task:
    return create_task(
        agent=agent,
        description=f"""
You are the Academic Research Specialist.

Research question:
{question}

Research plan:
{plan}

The academic-search system retrieved:

{academic_evidence}

Analyze the academic evidence according to the research plan.

Identify the most relevant scholarly findings.

For each important work provide:
- Finding
- Paper
- Year
- URL/DOI
- Important limitation if available

Do not invent papers.
Do not write a full literature review.
Be concise.
""",
        expected_output="""
A compact academic evidence dossier containing the strongest
relevant scholarly findings and source references.
""",
    )


def industry_research_task(
    agent,
    question: str,
    plan: str,
    industry_evidence: str,
) -> Task:
    return create_task(
        agent=agent,
        description=f"""
You are the Industry Research Specialist.

Research question:
{question}

Research plan:
{plan}

Industry/web evidence retrieved for industry research:

{industry_evidence}

Analyze the evidence for:
- companies
- products
- deployments
- adoption
- real-world implementations
- industry trends

Clearly distinguish company claims from independently supported evidence.

Return only the most useful findings.

Do not write the final report.
Be concise.
""",
        expected_output="""
A compact industry evidence dossier with important findings,
organizations and source URLs.
""",
    )


def evidence_analysis_task(
    agent,
    question: str,
    plan: str,
    web_findings: str,
    academic_findings: str,
    industry_findings: str,
) -> Task:
    return create_task(
        agent=agent,
        description=f"""
You are the Evidence Analyst.

Research question:
{question}

Research plan:
{plan}

WEB FINDINGS:
{web_findings}

ACADEMIC FINDINGS:
{academic_findings}

INDUSTRY FINDINGS:
{industry_findings}

Cross-analyze the research.

For each major claim determine:

Claim:
Supporting sources:
Cross-source agreement:
Contradiction:
Evidence strength:
Research gap:

Prioritize findings supported by multiple independent sources.

Do not introduce new facts.
Do not write the final report.

Be concise.
""",
        expected_output="""
A compact evidence map showing:
- strongest claims
- supporting sources
- cross-source agreement
- contradictions
- evidence gaps
""",
    )


def fact_check_task(
    agent,
    question: str,
    evidence_map: str,
) -> Task:
    return create_task(
        agent=agent,
        description=f"""
You are the Fact Checker for a multi-agent research system.

Research question:
{question}

EVIDENCE ANALYSIS:
{evidence_map}

Your job is to verify the important claims identified by the Evidence Analyst.

For every important claim, determine:

1. Does the cited source actually exist?
2. Does the source actually support the claim?
3. Is the claim stronger or more specific than the evidence?
4. Is the source primary, peer-reviewed, secondary, vendor-provided, or otherwise limited?
5. Are numerical/statistical claims explicitly supported?
6. Are paper titles, authors, publication venues and dates consistent with the available evidence?
7. Are there contradictions between sources?
8. Is the claim verified, partially verified, unsupported, or unverified?

Use this verification classification:

VERIFIED:
The source exists and directly supports the claim.

PARTIALLY VERIFIED:
The source supports the general idea but not the full strength, number, scope, or wording of the claim.

UNSUPPORTED:
The available evidence does not support the claim.

UNVERIFIED:
The claim may be plausible, but the source/evidence cannot be adequately verified.

IMPORTANT RULES:

- Never invent a citation.
- Never invent a paper title.
- Never invent authors.
- Never invent publication venues.
- Never invent statistics.
- Never upgrade a weak source into strong evidence.
- Never treat a vendor marketing claim as independent evidence.
- If a source does not explicitly support a numerical claim, mark that claim PARTIALLY VERIFIED or UNSUPPORTED.
- If a citation cannot be verified from the supplied evidence, mark it UNVERIFIED.
- Preserve uncertainty.
- Do not "repair" missing evidence by guessing.
- Do not introduce new unsupported facts.

Return a concise verification report.

Use this structure:

# Verification Summary

# Verified Claims

# Partially Verified Claims

# Unsupported or Unverified Claims

# Citation Issues

# Recommended Corrections

For each important claim, include:

- Claim
- Verification status
- Evidence/source
- Reason
- Required correction, if any

Do not write the final research report.
Your output is verification evidence for the Research Synthesizer.
""",
        expected_output="""
A concise fact-checking report that clearly classifies important claims as:
VERIFIED, PARTIALLY VERIFIED, UNSUPPORTED, or UNVERIFIED,
with source-based reasoning and recommended corrections.
""",
    )


def synthesis_task(
    agent,
    question: str,
    plan: str,
    evidence_map: str,
    fact_check: str,
) -> Task:
    return create_task(
        agent=agent,
        description=f"""
You are the Senior Research Synthesizer.

Research question:
{question}

Research plan:
{plan}

EVIDENCE ANALYSIS:
{evidence_map}

FACT CHECK RESULTS:
{fact_check}

Produce the final research report.

Use only the supplied research evidence.

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
- Do not treat unverified claims as established facts.
- Preserve important contradictions.
- Clearly distinguish company claims from independently supported findings.
- Include source URLs available in the evidence.
- Prefer conclusions supported by multiple evidence streams.
- Use clean Markdown only.
- Do not use HTML tags such as <br>, <div>, <span>, etc.
- Do not escape HTML tags.
- Keep tables valid Markdown.
- Use tables only when they materially improve clarity.
- Prefer concise headings and bullet points for detailed evidence.
- Do not repeat the same finding in multiple sections.
- Include only the most important findings.
- Keep the report concise enough to fit the available output budget.
- Every section must be completed.
- Do not stop midway through a section.

Write a professional research report.
""",
        expected_output="""
A polished research report with:
- executive summary
- key findings
- evidence analysis
- uncertainty
- practical implications
- conclusion
- source URLs
""",
    )
