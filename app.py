import os
import html

import streamlit as st

from crew.research_crew import ResearchCrew
from utils.formatting import clean_markdown, extract_sources


# =========================================================
# Load Streamlit Secrets
# =========================================================

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if "TAVILY_API_KEY" in st.secrets:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# Custom CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background: #F5F7FA;
}

.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Header */

.app-header {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 24px;
}

.app-title {
    font-size: 32px;
    font-weight: 700;
    color: #172033;
    margin: 0;
}

.app-subtitle {
    font-size: 15px;
    color: #667085;
    margin-top: 8px;
    line-height: 1.6;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E4E7EC;
}

/* Research report */

.report-container {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 14px;
    padding: 30px 34px;
    margin-top: 24px;
}

/* Source cards */

.source-card {
    background: #FFFFFF;
    border: 1px solid #E4E7EC;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
}

.source-title {
    font-size: 14px;
    font-weight: 600;
    color: #172033;
    margin-bottom: 5px;
}

.source-url {
    font-size: 12px;
    color: #175CD3;
    word-break: break-word;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 8px;
    min-height: 44px;
    font-weight: 600;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.markdown("## Research Settings")

    st.caption(
        "Configure the depth of the multi-agent research workflow."
    )

    research_depth = st.selectbox(
        "Research depth",
        ["Quick", "Standard", "Deep"],
        index=1,
        help=(
            "Quick uses fewer sources. Standard provides balanced "
            "research. Deep searches a larger evidence set."
        ),
    )

    st.divider()

    st.markdown("### Research modes")

    st.markdown(
        """
**Quick**

Fast exploratory research with a small evidence set.

**Standard**

Balanced research across web, academic and industry sources.

**Deep**

Broader evidence collection for detailed questions.
"""
    )

    st.divider()

    st.markdown("### Research Team")

    st.markdown(
        """
- Research Planner
- Web Researcher
- Academic Researcher
- Industry Researcher
- Evidence Analyst
- Fact Checker
- Research Synthesizer
"""
    )


# =========================================================
# Header
# =========================================================

st.markdown(
    """
<div class="app-header">
    <div class="app-title">Research Intelligence</div>
    <div class="app-subtitle">
        A multi-agent research system that plans investigations,
        gathers evidence, verifies important claims and produces
        structured research reports.
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# Research Question
# =========================================================

st.markdown("### Research Question")

question = st.text_area(
    "Enter your research question",
    placeholder=(
        "Example: What are the risks of AI in the developer field?"
    ),
    height=130,
    label_visibility="collapsed",
)


# =========================================================
# Start Research
# =========================================================

start_research = st.button(
    "Start Research",
    type="primary",
    use_container_width=True,
)


if start_research:

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    if not question.strip():
        st.warning(
            "Please enter a research question before starting."
        )
        st.stop()

    if not os.getenv("GROQ_API_KEY"):
        st.error(
            "GROQ_API_KEY is not configured in Streamlit Secrets."
        )
        st.stop()

    if not os.getenv("TAVILY_API_KEY"):
        st.warning(
            "TAVILY_API_KEY is not configured. "
            "Web research may be limited."
        )

    # -----------------------------------------------------
    # Progress
    # -----------------------------------------------------

    st.markdown("### Research Progress")

    progress = st.status(
        "Research team is working...",
        expanded=True,
    )

    try:

        progress.write(
            "Research Planner is creating the investigation plan."
        )

        progress.write(
            "Web, academic and industry researchers are gathering evidence."
        )

        progress.write(
            "Evidence Analyst is comparing collected findings."
        )

        progress.write(
            "Fact Checker is verifying important claims."
        )

        progress.write(
            "Research Synthesizer is preparing the final report."
        )

        # -------------------------------------------------
        # Run Crew
        # -------------------------------------------------

        research_crew = ResearchCrew()

        result = research_crew.run(
            question=question.strip(),
            depth=research_depth,
        )

        progress.update(
            label="Research completed",
            state="complete",
            expanded=False,
        )

        # -------------------------------------------------
        # Clean result
        # -------------------------------------------------

        report = clean_markdown(
            str(result)
        )

        # -------------------------------------------------
        # Report
        # -------------------------------------------------

        st.markdown(
            """
<div class="report-container">
""",
            unsafe_allow_html=True,
        )

        st.markdown("## Research Report")

        st.markdown(report)

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        sources = extract_sources(report)

        if sources:

            st.markdown("## Sources")

            for source in sources:

                title = html.escape(
                    source.get("title", "Source")
                )

                url = html.escape(
                    source.get("url", ""),
                    quote=True,
                )

                st.markdown(
                    f"""
<div class="source-card">
    <div class="source-title">
        {title}
    </div>
    <div class="source-url">
        {url}
    </div>
</div>
""",
                    unsafe_allow_html=True,
                )

    except Exception as exc:

        progress.update(
            label="Research could not be completed",
            state="error",
            expanded=False,
        )

        error_text = str(exc)

        if (
            "rate_limit" in error_text.lower()
            or "ratelimit" in error_text.lower()
            or "429" in error_text
        ):

            st.error(
                "The research workflow reached the current "
                "Groq token-per-minute limit."
            )

            st.info(
                "Wait for the rate-limit window to reset and "
                "try Quick research first."
            )

        else:

            st.error(
                "The research workflow could not be completed."
            )

        with st.expander("Technical details"):
            st.code(error_text)


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "Research Intelligence · Multi-Agent Research System"
)

st.caption(
    "AI-generated research should be verified against "
    "the cited sources before high-stakes use."
)
