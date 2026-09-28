import os
import html
import streamlit as st

from crew.research_crew import ResearchCrew
from utils.formatting import clean_markdown, extract_sources


# ---------------------------------------------------------
# Load secrets from Streamlit
# ---------------------------------------------------------

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if "TAVILY_API_KEY" in st.secrets:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Main application */

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
        letter-spacing: -0.5px;
    }

    .app-subtitle {
        font-size: 15px;
        color: #667085;
        margin-top: 8px;
        margin-bottom: 0;
        line-height: 1.6;
    }


    /* Research question card */

    .question-label {
        font-size: 15px;
        font-weight: 600;
        color: #344054;
        margin-bottom: 8px;
    }


    /* Status cards */

    .status-card {
        background: #FFFFFF;
        border: 1px solid #E4E7EC;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }

    .status-title {
        color: #175CD3;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 4px;
    }

    .status-text {
        color: #667085;
        font-size: 13px;
        margin: 0;
    }


    /* Report */

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
        margin-bottom: 4px;
    }

    .source-url {
        font-size: 12px;
        color: #175CD3;
        word-break: break-word;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E4E7EC;
    }

    .sidebar-title {
        font-size: 18px;
        font-weight: 700;
        color: #172033;
        margin-bottom: 4px;
    }

    .sidebar-description {
        font-size: 13px;
        color: #667085;
        line-height: 1.5;
        margin-bottom: 22px;
    }


    /* Buttons */

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        min-height: 44px;
        font-weight: 600;
    }


    /* Footer */

    .footer {
        text-align: center;
        color: #98A2B3;
        font-size: 12px;
        margin-top: 36px;
        padding-top: 20px;
        border-top: 1px solid #E4E7EC;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            Research Settings
        </div>

        <div class="sidebar-description">
            Configure the depth of the multi-agent research workflow.
        </div>
        """,
        unsafe_allow_html=True,
    )

    research_depth = st.selectbox(
        "Research depth",
        ["Quick", "Standard", "Deep"],
        index=1,
        help=(
            "Quick uses fewer sources and is faster. "
            "Standard provides balanced research. "
            "Deep searches a larger number of sources."
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
        Broader evidence collection for more detailed questions.
        """
    )

    st.divider()

    st.markdown(
        """
        **Research Team**

        7 specialized AI agents

        • Research Planner  
        • Web Researcher  
        • Academic Researcher  
        • Industry Researcher  
        • Evidence Analyst  
        • Fact Checker  
        • Research Synthesizer
        """
    )


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    """
    <div class="app-header">

        <h1 class="app-title">
            Research Intelligence
        </h1>

        <p class="app-subtitle">
            A multi-agent research system that plans investigations,
            gathers evidence, verifies important claims and produces
            structured research reports.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Research question
# ---------------------------------------------------------

st.markdown(
    '<div class="question-label">Research Question</div>',
    unsafe_allow_html=True,
)

question = st.text_area(
    "Research Question",
    placeholder=(
        "Example: What are the risks of AI in the developer field?"
    ),
    height=130,
    label_visibility="collapsed",
)


# ---------------------------------------------------------
# Start research button
# ---------------------------------------------------------

start_research = st.button(
    "Start Research",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

if start_research:

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
            "Web research may be unavailable or limited."
        )


    # -----------------------------------------------------
    # Workflow status
    # -----------------------------------------------------

    st.markdown(
        "### Research Progress"
    )

    status_placeholder = st.empty()


    with st.spinner(
        "The research team is working..."
    ):

        try:

            status_placeholder.markdown(
                """
                <div class="status-card">

                    <div class="status-title">
                        Research Planner
                    </div>

                    <p class="status-text">
                        Creating the investigation plan.
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )


            status_placeholder.markdown(
                """
                <div class="status-card">

                    <div class="status-title">
                        Research Team
                    </div>

                    <p class="status-text">
                        Web, academic and industry researchers
                        are gathering evidence.
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )


            research_crew = ResearchCrew()


            result = research_crew.run(
                question=question.strip(),
                depth=research_depth,
            )


            status_placeholder.markdown(
                """
                <div class="status-card">

                    <div class="status-title">
                        Research Complete
                    </div>

                    <p class="status-text">
                        Evidence has been analyzed, checked
                        and synthesized into the final report.
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )


            # -------------------------------------------------
            # Clean result
            # -------------------------------------------------

            report = clean_markdown(
                str(result)
            )


            # -------------------------------------------------
            # Final report
            # -------------------------------------------------

            st.markdown(
                """
                <div class="report-container">
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                "## Research Report"
            )

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

                st.markdown(
                    "## Sources"
                )

                for source in sources:

                    title = html.escape(
                        source.get(
                            "title",
                            "Source",
                        )
                    )

                    url = html.escape(
                        source.get(
                            "url",
                            "",
                        ),
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

            status_placeholder.empty()

            error_text = str(exc)

            if (
                "rate_limit" in error_text.lower()
                or "ratelimit" in error_text.lower()
                or "429" in error_text
            ):

                st.error(
                    """
                    The research workflow reached the current
                    Groq token limit. Please wait a few seconds
                    and try again with Quick or Standard research.
                    """
                )

                with st.expander(
                    "Technical details"
                ):
                    st.code(
                        error_text
                    )

            else:

                st.error(
                    "The research workflow could not be completed."
                )

                with st.expander(
                    "Technical details"
                ):
                    st.code(
                        error_text
                    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Research Intelligence · Multi-Agent Research System
        <br>
        AI-generated research should be verified against
        the cited sources before high-stakes use.
    </div>
    """,
    unsafe_allow_html=True,
)
