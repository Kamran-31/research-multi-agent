import os
import html
import streamlit as st

from crew.research_crew import ResearchCrew
from utils.formatting import clean_markdown, extract_sources


# ============================================================
# ENVIRONMENT
# ============================================================

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if "TAVILY_API_KEY" in st.secrets:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM UI
# ============================================================

st.html(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ========================================================
       GLOBAL
       ======================================================== */

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 12% 4%,
                rgba(38, 132, 255, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 88% 10%,
                rgba(0, 212, 255, 0.08),
                transparent 25%
            ),
            #070B12;

        color: #E8EDF5;
    }

    .block-container {
        max-width: 1380px;
        padding-top: 2.2rem;
        padding-bottom: 5rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0A0F18 0%,
                #080C14 100%
            );

        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.6rem 1.15rem;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #98A2B3 !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #748197 !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 32px;
    }

    .sidebar-logo {
        width: 42px;
        height: 42px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #2878FF,
                #00C6FF
            );

        color: white;

        font-size: 21px;
        font-weight: 700;

        box-shadow:
            0 9px 28px rgba(29,110,255,0.30);
    }

    .sidebar-brand-name {
        font-family: 'Space Grotesk', sans-serif;

        font-weight: 600;
        font-size: 16px;

        color: #F5F7FA;
    }

    .sidebar-section {
        margin-top: 27px;
        margin-bottom: 12px;

        font-size: 11px;
        font-weight: 700;

        letter-spacing: 1.6px;
        text-transform: uppercase;

        color: #667085;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background: #101722 !important;
        border: 1px solid #202B3A !important;
        border-radius: 11px !important;

        min-height: 45px !important;
    }

    div[data-baseweb="select"] span {
        color: #E8EDF5 !important;
        font-size: 14px !important;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero {
        position: relative;
        overflow: hidden;

        padding: 54px 52px 48px;

        border-radius: 25px;

        background:
            linear-gradient(
                135deg,
                rgba(18, 28, 44, 0.98),
                rgba(8, 15, 26, 0.98)
            );

        border: 1px solid rgba(255,255,255,0.085);

        box-shadow:
            0 30px 85px rgba(0,0,0,0.34);

        margin-bottom: 25px;
    }

    .hero::before {
        content: "";

        position: absolute;

        width: 500px;
        height: 500px;

        top: -290px;
        right: -90px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(0, 167, 255, 0.20),
                transparent 67%
            );

        pointer-events: none;
    }

    .hero::after {
        content: "";

        position: absolute;

        width: 340px;
        height: 340px;

        bottom: -270px;
        left: 22%;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(29,110,255,0.13),
                transparent 70%
            );

        pointer-events: none;
    }

    .hero-eyebrow {
        position: relative;
        z-index: 1;

        display: inline-flex;
        align-items: center;
        gap: 9px;

        padding: 8px 14px;

        border-radius: 100px;

        background: rgba(29,110,255,0.10);
        border: 1px solid rgba(29,110,255,0.25);

        color: #78B4FF;

        font-size: 12px;
        font-weight: 700;

        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    .hero-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #35D39A;

        box-shadow:
            0 0 13px rgba(53,211,154,0.8);
    }

    .hero-title {
        position: relative;
        z-index: 1;

        margin-top: 20px;

        font-family: 'Space Grotesk', sans-serif;

        font-size: clamp(44px, 5.5vw, 70px);

        line-height: 1.02;

        font-weight: 700;

        letter-spacing: -2.8px;

        background:
            linear-gradient(
                110deg,
                #FFFFFF 10%,
                #BBD7FF 48%,
                #67D9FF 90%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        position: relative;
        z-index: 1;

        max-width: 800px;

        margin-top: 20px;

        color: #A2AFC0;

        font-size: 17px;
        line-height: 1.75;
    }

    .hero-meta {
        position: relative;
        z-index: 1;

        display: flex;
        gap: 11px;
        flex-wrap: wrap;

        margin-top: 29px;
    }

    .meta-pill {
        padding: 8px 13px;

        border-radius: 8px;

        background: rgba(255,255,255,0.045);

        border: 1px solid rgba(255,255,255,0.08);

        color: #B2BDCC;

        font-size: 12px;
        font-weight: 500;
    }


    /* ========================================================
       SECTION LABELS
       ======================================================== */

    .section-label {
        margin-top: 38px;
        margin-bottom: 10px;

        color: #64748B;

        font-size: 11px;
        font-weight: 700;

        letter-spacing: 1.8px;
        text-transform: uppercase;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;

        color: #F5F7FA;

        font-size: 25px;
        font-weight: 600;

        margin-bottom: 18px;
    }


    /* ========================================================
       INPUT
       ======================================================== */

    .input-shell {
        padding: 2px;

        border-radius: 18px;

        background:
            linear-gradient(
                120deg,
                rgba(45,125,255,0.70),
                rgba(0,205,255,0.20),
                rgba(255,255,255,0.06)
            );

        box-shadow:
            0 16px 55px rgba(0,0,0,0.28);
    }

    .input-inner {
        background: #0D141F;
        border-radius: 16px;
        padding: 4px;
    }

    .stTextArea textarea {
        background: #0D141F !important;

        color: #E8EDF5 !important;

        border: none !important;

        border-radius: 15px !important;

        font-family: 'DM Sans', sans-serif !important;

        font-size: 17px !important;

        line-height: 1.65 !important;

        padding: 20px !important;

        min-height: 165px !important;

        box-shadow: none !important;
    }

    .stTextArea textarea:focus {
        border: none !important;

        box-shadow:
            0 0 0 1px rgba(60,145,255,0.30) !important;
    }

    .stTextArea textarea::placeholder {
        color: #536174 !important;
    }


    /* ========================================================
       BUTTON
       ======================================================== */

    .stButton > button {
        border: none !important;

        border-radius: 12px !important;

        min-height: 52px !important;

        padding: 0 25px !important;

        background:
            linear-gradient(
                135deg,
                #2878FF,
                #159BD7
            ) !important;

        color: #FFFFFF !important;

        font-family: 'DM Sans', sans-serif !important;

        font-size: 15px !important;

        font-weight: 700 !important;

        box-shadow:
            0 11px 30px rgba(25,113,255,0.28) !important;

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 16px 40px rgba(25,113,255,0.40) !important;
    }


    /* ========================================================
       MODE CARDS
       ======================================================== */

    .mode-card {
        padding: 20px;

        border-radius: 14px;

        background: #0D141F;

        border: 1px solid #1D2938;

        min-height: 116px;

        transition: all 0.2s ease;
    }

    .mode-card:hover {
        transform: translateY(-2px);

        border-color: #2C70C9;

        background: #101A28;
    }

    .mode-card.active {
        border-color: rgba(48,133,255,0.58);

        background:
            linear-gradient(
                145deg,
                rgba(25,75,140,0.24),
                rgba(13,20,31,0.95)
            );

        box-shadow:
            0 10px 30px rgba(20,100,220,0.08);
    }

    .mode-name {
        color: #F1F5F9;

        font-size: 15px;
        font-weight: 700;
    }

    .mode-subtitle {
        color: #579BEA;

        font-size: 11px;

        margin-top: 4px;

        font-weight: 600;
    }

    .mode-description {
        color: #7C899C;

        font-size: 13px;

        line-height: 1.55;

        margin-top: 9px;
    }


    /* ========================================================
       PIPELINE
       ======================================================== */

    .pipeline-container {
        padding: 25px;

        border-radius: 19px;

        background:
            linear-gradient(
                145deg,
                rgba(13,20,31,0.95),
                rgba(9,15,24,0.92)
            );

        border: 1px solid rgba(255,255,255,0.075);

        margin-top: 13px;
    }

    .pipeline {
        display: flex;
        align-items: center;

        gap: 8px;

        overflow-x: auto;

        padding-bottom: 5px;
    }

    .pipeline-node {
        min-width: 125px;

        padding: 16px 13px;

        text-align: center;

        border-radius: 12px;

        background: #111A27;

        border: 1px solid #202D3D;

        transition: all 0.2s ease;
    }

    .pipeline-node:hover {
        border-color: rgba(45,125,255,0.58);

        background: #142033;

        transform: translateY(-2px);
    }

    .pipeline-icon {
        font-size: 19px;

        color: #5EAEFF;

        margin-bottom: 8px;
    }

    .pipeline-name {
        color: #D7DFEA;

        font-size: 12px;
        font-weight: 600;

        line-height: 1.35;
    }

    .pipeline-arrow {
        color: #3A485B;

        font-size: 18px;

        flex-shrink: 0;
    }


    /* ========================================================
       STATUS
       ======================================================== */

    .status-panel {
        padding: 23px;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                #0D1623,
                #0B121C
            );

        border: 1px solid rgba(255,255,255,0.075);
    }

    .status-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        margin-bottom: 18px;
    }

    .status-title {
        color: #F1F5F9;

        font-family: 'Space Grotesk', sans-serif;

        font-size: 17px;
        font-weight: 600;
    }

    .status-live {
        display: flex;
        align-items: center;
        gap: 8px;

        color: #4DD9A1;

        font-size: 11px;
        font-weight: 700;

        letter-spacing: 0.7px;
    }

    .live-dot {
        width: 8px;
        height: 8px;

        border-radius: 50%;

        background: #38D39F;

        box-shadow:
            0 0 11px rgba(56,211,159,0.75);
    }

    .agent-row {
        display: flex;
        align-items: center;

        gap: 13px;

        padding: 12px 0;

        border-bottom: 1px solid rgba(255,255,255,0.045);
    }

    .agent-row:last-child {
        border-bottom: none;
    }

    .agent-number {
        width: 29px;
        height: 29px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 8px;

        background: #111D2C;

        color: #73AEFF;

        font-size: 10px;
        font-weight: 700;
    }

    .agent-name {
        color: #C7D0DD;

        font-size: 13px;
        font-weight: 500;
    }

    .agent-state {
        margin-left: auto;

        color: #69788C;

        font-size: 11px;
    }


    /* ========================================================
       REPORT
       ======================================================== */

    .report-shell {
        margin-top: 28px;

        border-radius: 21px;

        background:
            linear-gradient(
                145deg,
                #0D141F,
                #0A111A
            );

        border: 1px solid rgba(255,255,255,0.075);

        overflow: hidden;

        box-shadow:
            0 25px 65px rgba(0,0,0,0.28);
    }

    .report-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        padding: 23px 27px;

        border-bottom: 1px solid rgba(255,255,255,0.065);
    }

    .report-header-title {
        display: flex;
        align-items: center;
        gap: 11px;

        color: #F3F6FA;

        font-family: 'Space Grotesk', sans-serif;

        font-size: 17px;
        font-weight: 600;
    }

    .report-mark {
        width: 31px;
        height: 31px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 8px;

        background: rgba(39,121,255,0.12);

        color: #69A9FF;
    }

    .report-badge {
        padding: 7px 10px;

        border-radius: 7px;

        background: rgba(53,211,154,0.08);

        border: 1px solid rgba(53,211,154,0.15);

        color: #4DD9A1;

        font-size: 10px;
        font-weight: 700;

        letter-spacing: 0.8px;
    }

    .report-content {
        padding: 34px;
    }

    .report-content h1,
    .report-content h2,
    .report-content h3 {
        font-family: 'Space Grotesk', sans-serif;

        color: #F4F7FA;
    }

    .report-content h1 {
        font-size: 30px;
    }

    .report-content h2 {
        font-size: 23px;

        margin-top: 32px;

        padding-bottom: 9px;

        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    .report-content h3 {
        font-size: 18px;
    }

    .report-content p,
    .report-content li {
        color: #AAB6C6;

        font-size: 15px;

        line-height: 1.8;
    }

    .report-content strong {
        color: #E8EEF6;
    }

    .report-content blockquote {
        border-left: 3px solid #2779FF;

        background: rgba(39,121,255,0.055);

        padding: 13px 17px;

        color: #AAB8CA;
    }

    .report-content code {
        background: #111B29;

        color: #7FC3FF;

        padding: 2px 6px;

        border-radius: 5px;
    }


    /* ========================================================
       SOURCE CARDS
       ======================================================== */

    .source-card {
        padding: 17px 19px;

        border-radius: 12px;

        background: #0D141F;

        border: 1px solid #1D2938;

        margin-bottom: 10px;

        transition: all 0.2s ease;
    }

    .source-card:hover {
        border-color: #285A91;

        transform: translateX(2px);
    }

    .source-title {
        color: #DCE4EE;

        font-size: 14px;
        font-weight: 600;

        margin-bottom: 7px;
    }

    .source-url {
        color: #579BEA;

        font-size: 12px;

        word-break: break-all;
    }


    /* ========================================================
       STREAMLIT STATUS
       ======================================================== */

    div[data-testid="stStatusWidget"] {
        background: #0D141F !important;

        border: 1px solid #1D2938 !important;

        border-radius: 14px !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;

        margin-top: 50px;

        padding-top: 24px;

        border-top: 1px solid rgba(255,255,255,0.06);

        color: #475467;

        font-size: 12px;

        line-height: 1.7;
    }

    div[data-testid="stTextArea"] {
    width: 100%;
    }

    div[data-testid="stTextArea"] > div {
        border: 1px solid rgba(45, 125, 255, 0.4) !important;
        border-radius: 16px !important;
        background: #0D141F !important;
        overflow: hidden !important;
    }

    div[data-testid="stTextArea"] textarea {
        background: transparent !important;
        border: none !important;
        border-radius: 16px !important;
        color: #E8EEF7 !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextArea"] textarea:focus {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    /* Question textarea fix */
    div[data-testid="stTextArea"] {
        width: 100%;
    )


    /* Mobile pipeline fix */
    @media (max-width: 768px) {
        .pipeline {
            flex-direction: column;
            align-items: stretch;
            overflow-x: visible;
        }

        .pipeline-node {
            width: 100%;
            max-width: none;
        }

        .pipeline-arrow {
            transform: rotate(90deg);
            align-self: center;
            margin: 4px 0;
        }
    }
    
    </style>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">◈</div>
            <div class="sidebar-brand-name">
                Research Intelligence
            </div>
        </div>
        """
    )

    st.html(
        '<div class="sidebar-section">Research Configuration</div>'
    )

    if "research_depth" not in st.session_state:
        st.session_state.research_depth = "Standard"

    if "selected_mode" in st.session_state:
        st.session_state.research_depth = st.session_state.selected_mode
        del st.session_state.selected_mode
    
    research_depth = st.selectbox(
        "Research depth",
        ["Quick", "Standard", "Deep"],
        index=["Quick", "Standard", "Deep"].index(
            st.session_state.research_depth
        ),
        label_visibility="collapsed",
    )

    depth_info = {
        "Quick": "Fast exploratory research with a compact evidence set.",
        "Standard": "Balanced investigation across multiple source categories.",
        "Deep": "Broader evidence collection for complex questions.",
    }

    st.caption(depth_info[research_depth])

    st.html(
        '<div class="sidebar-section">Research Sources</div>'
    )

    st.html(
        """
        <div style="
            line-height:2.15;
            color:#8794A7;
            font-size:13px;
        ">
            ◉ Web · Current information<br>
            ◉ Academic · Scholarly literature<br>
            ◉ Industry · Market evidence<br>
            ◉ Verification · Claim checking
        </div>
        """
    )

    st.html(
        '<div class="sidebar-section">Agent Team</div>'
    )

    agents = [
        "Research Planner",
        "Web Researcher",
        "Academic Researcher",
        "Industry Researcher",
        "Evidence Analyst",
        "Fact Checker",
        "Research Synthesizer",
    ]

    for i, agent in enumerate(agents, 1):

        st.html(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                margin:10px 0;
                color:#8794A7;
                font-size:13px;
            ">

                <span style="
                    width:23px;
                    height:23px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border-radius:7px;
                    background:#111A27;
                    color:#5D9FEF;
                    font-size:10px;
                    font-weight:700;
                ">
                    {i}
                </span>

                {agent}

            </div>
            """
        )

    st.html(
        '<div class="sidebar-section">System Status</div>'
    )

    groq_ready = bool(os.getenv("GROQ_API_KEY"))
    tavily_ready = bool(os.getenv("TAVILY_API_KEY"))

    groq_status = "Connected" if groq_ready else "Missing"
    tavily_status = "Connected" if tavily_ready else "Missing"

    groq_color = "#42D69C" if groq_ready else "#F97066"
    tavily_color = "#42D69C" if tavily_ready else "#F97066"

    st.html(
        f"""
        <div style="
            padding:15px;
            border-radius:11px;
            background:#0D141F;
            border:1px solid #1D2938;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:11px;
                color:#8794A7;
                font-size:13px;
            ">
                <span>LLM Service</span>

                <span style="
                    color:{groq_color};
                    font-weight:600;
                ">
                    {groq_status}
                </span>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                color:#8794A7;
                font-size:13px;
            ">
                <span>Web Search</span>

                <span style="
                    color:{tavily_color};
                    font-weight:600;
                ">
                    {tavily_status}
                </span>
            </div>

        </div>
        """
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-eyebrow">
            <span class="hero-dot"></span>
            Multi-Agent Research System
        </div>

        <div class="hero-title">
            Research Intelligence
        </div>

        <div class="hero-description">
            Turn complex questions into structured intelligence.
            Specialized AI agents investigate web, academic and
            industry evidence, analyze claims and synthesize the
            findings into a research report.
        </div>

        <div class="hero-meta">

            <div class="meta-pill">
                7 Specialized Agents
            </div>

            <div class="meta-pill">
                Multi-Source Research
            </div>

            <div class="meta-pill">
                Evidence Verification
            </div>

            <div class="meta-pill">
                Structured Reports
            </div>

        </div>

    </div>
    """
)


# ============================================================
# RESEARCH QUESTION
# ============================================================

st.html(
    """
    <div class="section-label">
        01 · Investigation
    </div>

    <div class="section-title">
        What do you want to investigate?
    </div>
    """
)

question = st.text_area(
    "Research question",
    placeholder=(
        "Ask a research question...\n\n"
        "Example: What are the major opportunities, risks and "
        "market trends for AI-powered cybersecurity platforms?"
    ),
    height=165,
    label_visibility="collapsed",
)


# ============================================================
# RESEARCH MODES
# ============================================================

st.html(
    """
    <div class="section-label">
        02 · Research Depth
    </div>

    <div class="section-title">
        Choose your investigation depth
    </div>
    """
)

mode_cols = st.columns(3)

mode_data = [
    (
        "Quick",
        "Fast exploration",
        "Compact evidence set for initial investigation.",
    ),
    (
        "Standard",
        "Balanced research",
        "Web, academic and industry relevant evidence.",
    ),
    (
        "Deep",
        "Extended investigation",
        "Broader evidence for complex questions.",
    ),
]


# ------------------------------------------------------------
# Dynamic styling for the three clickable mode cards
# ------------------------------------------------------------

active_index = {
    "Quick": 1,
    "Standard": 2,
    "Deep": 3,
}[research_depth]

st.html(
    f"""
    <style>

    /* Mode card buttons */

    div[data-testid="stHorizontalBlock"] > div:nth-child(1)
    div[data-testid="stButton"] > button,
    div[data-testid="stHorizontalBlock"] > div:nth-child(2)
    div[data-testid="stButton"] > button,
    div[data-testid="stHorizontalBlock"] > div:nth-child(3)
    div[data-testid="stButton"] > button {{
        width: 100% !important;
        min-height: 116px !important;

        padding: 20px !important;

        border-radius: 14px !important;

        background: #0D141F !important;

        border: 1px solid #1D2938 !important;

        color: #E8EDF5 !important;

        text-align: left !important;

        box-shadow: none !important;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            background 0.2s ease,
            box-shadow 0.2s ease !important;
    }}


    /* Hover */

    div[data-testid="stHorizontalBlock"] > div:nth-child(1)
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(2)
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stHorizontalBlock"] > div:nth-child(3)
    div[data-testid="stButton"] > button:hover {{
        transform: translateY(-2px) !important;

        border-color: #2C70C9 !important;

        background: #101A28 !important;

        color: #F1F5F9 !important;
    }}


    /* Active card */

    div[data-testid="stHorizontalBlock"] > div:nth-child({active_index})
    div[data-testid="stButton"] > button {{
        border-color: rgba(48,133,255,0.58) !important;

        background:
            linear-gradient(
                145deg,
                rgba(25,75,140,0.24),
                rgba(13,20,31,0.95)
            ) !important;

        box-shadow:
            0 10px 30px rgba(20,100,220,0.08) !important;
    }}


    /* Keep button text clean */

    div[data-testid="stHorizontalBlock"] > div
    div[data-testid="stButton"] > button p {{
        margin: 0 !important;

        color: #F1F5F9 !important;

        font-size: 14px !important;

        line-height: 1.55 !important;
    }}

    </style>
    """
)


# ------------------------------------------------------------
# Clickable mode cards
# ------------------------------------------------------------

for col, (name, subtitle, description) in zip(
    mode_cols,
    mode_data,
):

    with col:

        clicked = st.button(
            f"**{name}**  \n"
            f"{subtitle}  \n"
            f"{description}",
            key=f"mode_{name.lower()}",
            use_container_width=True,
        )

        if clicked:
            st.session_state.selected_mode = name
            st.rerun()


# ============================================================
# START
# ============================================================

st.html("<div style='height:18px'></div>")

start_research = st.button(
    "◈   Start Intelligence Research",
    type="primary",
    use_container_width=True,
)


# ============================================================
# PIPELINE
# ============================================================

st.html(
    """
    <div class="section-label">
        03 · Agent Architecture
    </div>

    <div class="section-title">
        Seven agents. One research workflow.
    </div>
    """
)

st.html(
    """
    <div class="pipeline-container">

        <div class="pipeline">

            <div class="pipeline-node">
                <div class="pipeline-icon">⌁</div>
                <div class="pipeline-name">
                    Research<br>Planner
                </div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">◉</div>
                <div class="pipeline-name">
                    Web<br>Researcher
                </div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">◇</div>
                <div class="pipeline-name">
                    Academic<br>Researcher
                </div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">▣</div>
                <div class="pipeline-name">
                    Industry<br>Researcher
                </div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">◎</div>
                <div class="pipeline-name">
                    Evidence<br>Analyst
                </div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">✓</div>
                <div class="pipeline-name">
                    Fact<br>Checker
                </div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">✦</div>
                <div class="pipeline-name">
                    Research<br>Synthesizer
                </div>
            </div>

        </div>

    </div>
    """
)


# ============================================================
# EXECUTION
# ============================================================

if start_research:

    if not question.strip():
        st.warning(
            "Enter a research question before starting the investigation."
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
            "Web and industry research may be limited."
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

        st.html(
    """
    <div class="section-label">
        04 · Live Workflow
    </div>
    """
)

# Dynamic workflow status container
workflow_status = st.empty()

# Initial state
workflow_status.html(
    """
    <div class="status-panel">

        <div class="status-header">

            <div class="status-title">
                Research Team
            </div>

            <div class="status-live">
                <span class="live-dot"></span>
                PROCESSING
            </div>

        </div>

        <div class="agent-row">
            <div class="agent-number">01</div>
            <div class="agent-name">Research Planner</div>
            <div class="agent-state">Waiting</div>
        </div>

        <div class="agent-row">
            <div class="agent-number">02</div>
            <div class="agent-name">Web Researcher</div>
            <div class="agent-state">Waiting</div>
        </div>

        <div class="agent-row">
            <div class="agent-number">03</div>
            <div class="agent-name">Academic Researcher</div>
            <div class="agent-state">Waiting</div>
        </div>

        <div class="agent-row">
            <div class="agent-number">04</div>
            <div class="agent-name">Industry Researcher</div>
            <div class="agent-state">Waiting</div>
        </div>

        <div class="agent-row">
            <div class="agent-number">05</div>
            <div class="agent-name">Evidence Analyst</div>
            <div class="agent-state">Waiting</div>
        </div>

        <div class="agent-row">
            <div class="agent-number">06</div>
            <div class="agent-name">Fact Checker</div>
            <div class="agent-state">Waiting</div>
        </div>

        <div class="agent-row">
            <div class="agent-number">07</div>
            <div class="agent-name">Research Synthesizer</div>
            <div class="agent-state">Waiting</div>
        </div>

    </div>
    """
)


def update_workflow_status(message):

    statuses = {
        1: ("Research Planner", "Planning"),
        2: ("Web Researcher", "Gathering evidence"),
        3: ("Academic Researcher", "Searching literature"),
        4: ("Industry Researcher", "Analyzing industry"),
        5: ("Evidence Analyst", "Comparing evidence"),
        6: ("Fact Checker", "Verifying claims"),
        7: ("Research Synthesizer", "Preparing report"),
    }

    active_agent = None

    for number, (agent_name, state) in statuses.items():
        if agent_name.lower() in message.lower():
            active_agent = number
            break

    if "Collecting web evidence" in message:
        active_agent = 2

    elif "Collecting academic evidence" in message:
        active_agent = 3

    elif "Collecting industry evidence" in message:
        active_agent = 4

    rows = []

    for number, (agent_name, state) in statuses.items():

        if active_agent == number:
            current_state = state
        elif active_agent and number < active_agent:
            current_state = "Completed"
        else:
            current_state = "Waiting"

        rows.append(
            f"""
            <div class="agent-row">
                <div class="agent-number">0{number}</div>
                <div class="agent-name">{agent_name}</div>
                <div class="agent-state">{current_state}</div>
            </div>
            """
        )

    workflow_status.html(
        f"""
        <div class="status-panel">

            <div class="status-header">

                <div class="status-title">
                    Research Team
                </div>

                <div class="status-live">
                    <span class="live-dot"></span>
                    PROCESSING
                </div>

            </div>

            {''.join(rows)}

        </div>
        """
    )


progress = st.status(
    "Agents are conducting the investigation...",
    expanded=False,
)

try:

    research_crew = ResearchCrew()

    with progress:

        def status_callback(message):

            update_workflow_status(message)

            st.write(message)

        result = research_crew.run(
            question=question.strip(),
            depth=research_depth,
            status_callback=status_callback,
        )

    # Final UI state
    workflow_status.html(
        """
        <div class="status-panel">

            <div class="status-header">

                <div class="status-title">
                    Research Team
                </div>

                <div class="status-live">
                    <span class="live-dot"></span>
                    COMPLETE
                </div>

            </div>

            <div class="agent-row">
                <div class="agent-number">01</div>
                <div class="agent-name">Research Planner</div>
                <div class="agent-state">Completed</div>
            </div>

            <div class="agent-row">
                <div class="agent-number">02</div>
                <div class="agent-name">Web Researcher</div>
                <div class="agent-state">Completed</div>
            </div>

            <div class="agent-row">
                <div class="agent-number">03</div>
                <div class="agent-name">Academic Researcher</div>
                <div class="agent-state">Completed</div>
            </div>

            <div class="agent-row">
                <div class="agent-number">04</div>
                <div class="agent-name">Industry Researcher</div>
                <div class="agent-state">Completed</div>
            </div>

            <div class="agent-row">
                <div class="agent-number">05</div>
                <div class="agent-name">Evidence Analyst</div>
                <div class="agent-state">Completed</div>
            </div>

            <div class="agent-row">
                <div class="agent-number">06</div>
                <div class="agent-name">Fact Checker</div>
                <div class="agent-state">Completed</div>
            </div>

            <div class="agent-row">
                <div class="agent-number">07</div>
                <div class="agent-name">Research Synthesizer</div>
                <div class="agent-state">Completed</div>
            </div>

        </div>
        """
    )

    progress.update(
        label="Research completed successfully",
        state="complete",
        expanded=False,
    )

        # ----------------------------------------------------
        # REPORT
        # ----------------------------------------------------

        report = clean_markdown(str(result))

        st.html(
            """
            <div class="section-label">
                05 · Intelligence Report
            </div>

            <div class="report-shell">

                <div class="report-header">

                    <div class="report-header-title">

                        <div class="report-mark">
                            ✦
                        </div>

                        Research Intelligence Report

                    </div>

                    <div class="report-badge">
                        COMPLETED
                    </div>

                </div>

                <div class="report-content">
            """
        )

        st.markdown(report)

        st.html(
            """
                </div>
            </div>
            """
        )

        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        sources = extract_sources(report)

        if sources:

            st.html(
                """
                <div class="section-label">
                    06 · Evidence Base
                </div>

                <div class="section-title">
                    Research Sources
                </div>
                """
            )

            for source in sources:

                title = html.escape(
                    source.get("title", "Source")
                )

                url = html.escape(
                    source.get("url", ""),
                    quote=True,
                )

                st.html(
                    f"""
                    <div class="source-card">

                        <div class="source-title">
                            {title}
                        </div>

                        <div class="source-url">
                            {url}
                        </div>

                    </div>
                    """
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
                "Try Quick research after the current "
                "rate-limit window resets."
            )

        else:

            st.error(
                "The research workflow could not be completed."
            )

        with st.expander("Technical details"):
            st.code(error_text)


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        Research Intelligence · Multi-Agent Research System

        <br>

        AI-generated research should be verified against
        cited sources before high-stakes use.

    </div>
    """
)
