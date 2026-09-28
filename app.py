import os

import streamlit as st

from crew.research_crew import ResearchCrew
from utils.formatting import clean_markdown, extract_sources


st.set_page_config(
    page_title="Research Intelligence",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Load Streamlit secrets into environment variables
# ---------------------------------------------------------

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if "TAVILY_API_KEY" in st.secrets:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    :root {
        --background: #F5F7FA;
        --surface: #FFFFFF;
        --border: #D9DEE7;
        --text: #172033;
        --muted: #667085;
        --accent: #175CD3;
        --accent-dark: #1849A9;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--text);
        letter-spacing: -0.02em;
    }

    .kicker {
        color: var(--accent);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .subtitle {
        color: var(--muted);
        max-width: 760px;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .report-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.4rem;
        margin-top: 1rem;
    }

    .source-item {
        border-top: 1px solid var(--border);
        padding: 0.8rem 0;
    }

    .source-item:first-child {
        border-top: 0;
    }

    .source-title {
        font-weight: 650;
        color: var(--text);
    }

    .source-url {
        color: var(--accent);
        font-size: 0.86rem;
        word-break: break-word;
    }

    div.stButton > button {
        border-radius: 7px;
        border: 1px solid var(--accent);
        background: var(--accent);
        color: white;
        font-weight: 650;
    }

    div.stButton > button:hover {
        background: var(--accent-dark);
        border-color: var(--accent-dark);
    }

    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="kicker">Research Intelligence</div>',
    unsafe_allow_html=True,
)

st.title("Multi-Agent Research Assistant")

st.markdown(
    """
    <div class="subtitle">
    A seven-agent research workflow that plans an investigation,
    gathers web, academic and industry evidence, checks important
    claims, and produces a source-grounded research report.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("Research settings")

    depth = st.selectbox(
        "Research depth",
        [
            "Focused",
            "Standard",
            "Comprehensive",
        ],
        index=1,
    )

    max_results = st.slider(
        "Results per search",
        min_value=3,
        max_value=8,
        value=5,
    )

    st.divider()

    st.caption(
        "CrewAI orchestrates the agents. "
        "Groq powers reasoning. "
        "Tavily provides web research. "
        "OpenAlex provides academic literature."
    )


# ---------------------------------------------------------
# Input
# ---------------------------------------------------------

question = st.text_area(
    "Research question",
    placeholder=(
        "Example: What are the opportunities, risks and "
        "current applications of AI-powered cybersecurity?"
    ),
    height=130,
)


start = st.button(
    "Start research",
    use_container_width=True,
)


# ---------------------------------------------------------
# Research
# ---------------------------------------------------------

if start:

    if not question.strip():
        st.warning(
            "Enter a research question before starting."
        )
        st.stop()

    if not os.getenv("GROQ_API_KEY"):
        st.error(
            "GROQ_API_KEY is not configured. "
            "Add it to Streamlit Secrets."
        )
        st.stop()

    with st.status(
        "Research team is working...",
        expanded=True,
    ) as status:

        st.write(
            "Research Planner is creating the investigation plan."
        )

        st.write(
            "Web, academic and industry researchers are gathering evidence."
        )

        st.write(
            "Evidence Analyst is comparing the collected findings."
        )

        st.write(
            "Fact Checker is verifying important claims."
        )

        st.write(
            "Research Synthesizer is preparing the final report."
        )

        try:

            research_crew = ResearchCrew()

            result = research_crew.run(
                question=question.strip(),
                depth=depth,
                max_results=max_results,
            )

            status.update(
                label="Research completed",
                state="complete",
                expanded=False,
            )

        except Exception as exc:

            status.update(
                label="Research failed",
                state="error",
                expanded=True,
            )

            st.error(
                "The research workflow could not be completed."
            )

            st.exception(exc)

            st.stop()


    # -----------------------------------------------------
    # Report
    # -----------------------------------------------------

    report = clean_markdown(result)

    st.markdown(
        '<div class="report-card">',
        unsafe_allow_html=True,
    )

    st.markdown("## Research report")

    st.markdown(report)

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # -----------------------------------------------------
    # Sources
    # -----------------------------------------------------

    sources = extract_sources(result)

    if sources:

        st.markdown("## Sources")

        for source in sources:

            st.markdown(
                f"""
                <div class="source-item">
                    <div class="source-title">
                        {source["title"]}
                    </div>
                    <div class="source-url">
                        {source["url"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


st.caption(
    "Research results should be reviewed against the cited sources "
    "before being used for high-stakes decisions."
)
