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
# PREMIUM UI STYLES
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');


/* =========================================================
   GLOBAL
   ========================================================= */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            rgba(38, 132, 255, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 12%,
            rgba(0, 212, 255, 0.07),
            transparent 25%
        ),
        #070B12;
    color: #E8EDF5;
}

.block-container {
    max-width: 1380px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}


/* =========================================================
   HIDE STREAMLIT CHROME
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

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
    padding: 1.5rem 1rem;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F2F5F9;
    font-family: 'Space Grotesk', sans-serif;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #98A2B3 !important;
}

section[data-testid="stSidebar"] .stCaption {
    color: #667085 !important;
}


/* =========================================================
   SIDEBAR BRAND
   ========================================================= */

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 28px;
}

.sidebar-logo {
    width: 38px;
    height: 38px;
    border-radius: 11px;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #1D6EFF,
            #00C6FF
        );

    color: white;
    font-size: 19px;
    font-weight: 700;

    box-shadow:
        0 8px 25px rgba(29,110,255,0.28);
}

.sidebar-brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 15px;
    color: #F5F7FA;
}


/* =========================================================
   SIDEBAR SECTION
   ========================================================= */

.sidebar-section {
    margin-top: 25px;
    margin-bottom: 10px;

    font-size: 10px;
    font-weight: 700;

    letter-spacing: 1.6px;
    text-transform: uppercase;

    color: #667085;
}


/* =========================================================
   SELECTBOX
   ========================================================= */

div[data-baseweb="select"] > div {
    background: #101722 !important;
    border: 1px solid #202B3A !important;
    border-radius: 10px !important;
    color: #E8EDF5 !important;
}

div[data-baseweb="select"] span {
    color: #E8EDF5 !important;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    position: relative;
    overflow: hidden;

    padding: 48px 48px 42px;

    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(18, 28, 44, 0.98),
            rgba(8, 15, 26, 0.98)
        );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 30px 80px rgba(0,0,0,0.30);

    margin-bottom: 22px;
}

.hero::before {
    content: "";

    position: absolute;

    width: 420px;
    height: 420px;

    top: -250px;
    right: -100px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(0, 167, 255, 0.18),
            transparent 65%
        );

    pointer-events: none;
}

.hero::after {
    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    bottom: -220px;
    left: 20%;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(29,110,255,0.12),
            transparent 70%
        );

    pointer-events: none;
}

.hero-eyebrow {
    position: relative;
    z-index: 1;

    display: inline-flex;
    align-items: center;
    gap: 8px;

    padding: 7px 12px;

    border-radius: 100px;

    background: rgba(29,110,255,0.10);
    border: 1px solid rgba(29,110,255,0.25);

    color: #72AEFF;

    font-size: 11px;
    font-weight: 700;

    letter-spacing: 1.4px;
    text-transform: uppercase;
}

.hero-dot {
    width: 6px;
    height: 6px;

    border-radius: 50%;

    background: #35D39A;

    box-shadow:
        0 0 12px rgba(53,211,154,0.7);
}

.hero-title {
    position: relative;
    z-index: 1;

    margin-top: 18px;

    font-family: 'Space Grotesk', sans-serif;

    font-size: clamp(38px, 5vw, 64px);

    line-height: 1.02;

    font-weight: 700;

    letter-spacing: -2.5px;

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

    max-width: 730px;

    margin-top: 17px;

    color: #98A6B8;

    font-size: 16px;
    line-height: 1.7;
}

.hero-meta {
    position: relative;
    z-index: 1;

    display: flex;
    gap: 10px;
    flex-wrap: wrap;

    margin-top: 25px;
}

.meta-pill {
    padding: 7px 11px;

    border-radius: 7px;

    background: rgba(255,255,255,0.045);

    border: 1px solid rgba(255,255,255,0.08);

    color: #AAB6C6;

    font-size: 12px;
}


/* =========================================================
   SECTION HEADERS
   ========================================================= */

.section-label {
    margin-top: 34px;
    margin-bottom: 12px;

    color: #667085;

    font-size: 10px;
    font-weight: 700;

    letter-spacing: 1.8px;
    text-transform: uppercase;
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;

    color: #F5F7FA;

    font-size: 22px;
    font-weight: 600;

    margin-bottom: 16px;
}


/* =========================================================
   RESEARCH INPUT
   ========================================================= */

.input-shell {
    padding: 2px;

    border-radius: 17px;

    background:
        linear-gradient(
            120deg,
            rgba(45,125,255,0.65),
            rgba(0,205,255,0.18),
            rgba(255,255,255,0.05)
        );

    box-shadow:
        0 15px 50px rgba(0,0,0,0.25);
}

.input-inner {
    background: #0D141F;

    border-radius: 15px;

    padding: 4px;
}


/* =========================================================
   TEXT AREA
   ========================================================= */

.stTextArea textarea {
    background: #0D141F !important;

    color: #E8EDF5 !important;

    border: none !important;

    border-radius: 14px !important;

    font-family: 'DM Sans', sans-serif !important;

    font-size: 16px !important;

    line-height: 1.6 !important;

    padding: 18px !important;

    min-height: 150px !important;

    box-shadow: none !important;
}

.stTextArea textarea:focus {
    border: none !important;

    box-shadow:
        0 0 0 1px rgba(60,145,255,0.3) !important;
}

.stTextArea textarea::placeholder {
    color: #536174 !important;
}


/* =========================================================
   PRIMARY BUTTON
   ========================================================= */

.stButton > button {
    border: none !important;

    border-radius: 11px !important;

    min-height: 48px !important;

    padding: 0 22px !important;

    background:
        linear-gradient(
            135deg,
            #2878FF,
            #159BD7
        ) !important;

    color: #FFFFFF !important;

    font-family: 'DM Sans', sans-serif !important;

    font-size: 14px !important;

    font-weight: 700 !important;

    box-shadow:
        0 10px 28px rgba(25,113,255,0.25) !important;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px);

    box-shadow:
        0 14px 35px rgba(25,113,255,0.38) !important;
}


/* =========================================================
   PIPELINE
   ========================================================= */

.pipeline-container {
    padding: 22px;

    border-radius: 18px;

    background: rgba(13,20,31,0.82);

    border: 1px solid rgba(255,255,255,0.07);

    margin-top: 12px;
}

.pipeline {
    display: flex;
    align-items: center;

    gap: 7px;

    overflow-x: auto;

    padding-bottom: 4px;
}

.pipeline-node {
    min-width: 116px;

    padding: 13px 12px;

    text-align: center;

    border-radius: 11px;

    background: #111A27;

    border: 1px solid #202D3D;

    transition: all 0.2s ease;
}

.pipeline-node:hover {
    border-color: rgba(45,125,255,0.55);

    background: #142033;
}

.pipeline-icon {
    font-size: 16px;

    color: #5EAEFF;

    margin-bottom: 6px;
}

.pipeline-name {
    color: #D7DFEA;

    font-size: 11px;
    font-weight: 600;

    line-height: 1.3;
}

.pipeline-arrow {
    color: #3A485B;

    font-size: 16px;

    flex-shrink: 0;
}


/* =========================================================
   MODE CARDS
   ========================================================= */

.mode-card {
    padding: 17px;

    border-radius: 13px;

    background: #0D141F;

    border: 1px solid #1D2938;

    height: 100%;

    transition: all 0.2s ease;
}

.mode-card:hover {
    transform: translateY(-2px);

    border-color: #2C70C9;

    background: #101A28;
}

.mode-card.active {
    border-color: rgba(48,133,255,0.55);

    background:
        linear-gradient(
            145deg,
            rgba(25,75,140,0.22),
            rgba(13,20,31,0.95)
        );
}

.mode-name {
    color: #F1F5F9;

    font-size: 13px;
    font-weight: 700;
}

.mode-description {
    color: #738197;

    font-size: 11px;

    line-height: 1.5;

    margin-top: 6px;
}


/* =========================================================
   STATUS
   ========================================================= */

.status-panel {
    padding: 20px;

    border-radius: 17px;

    background:
        linear-gradient(
            135deg,
            #0D1623,
            #0B121C
        );

    border: 1px solid rgba(255,255,255,0.07);
}

.status-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 17px;
}

.status-title {
    color: #F1F5F9;

    font-family: 'Space Grotesk', sans-serif;

    font-size: 15px;
    font-weight: 600;
}

.status-live {
    display: flex;
    align-items: center;
    gap: 7px;

    color: #4DD9A1;

    font-size: 11px;
    font-weight: 600;
}

.live-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #38D39F;

    box-shadow:
        0 0 10px rgba(56,211,159,0.75);
}

.agent-row {
    display: flex;
    align-items: center;

    gap: 12px;

    padding: 10px 0;

    border-bottom: 1px solid rgba(255,255,255,0.045);
}

.agent-row:last-child {
    border-bottom: none;
}

.agent-number {
    width: 26px;
    height: 26px;

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

    font-size: 12px;
}

.agent-state {
    margin-left: auto;

    color: #69788C;

    font-size: 10px;
}


/* =========================================================
   REPORT
   ========================================================= */

.report-shell {
    margin-top: 28px;

    border-radius: 20px;

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

    padding: 21px 25px;

    border-bottom: 1px solid rgba(255,255,255,0.065);
}

.report-header-title {
    display: flex;
    align-items: center;
    gap: 10px;

    color: #F3F6FA;

    font-family: 'Space Grotesk', sans-serif;

    font-size: 15px;
    font-weight: 600;
}

.report-mark {
    width: 28px;
    height: 28px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 8px;

    background: rgba(39,121,255,0.12);

    color: #69A9FF;
}

.report-badge {
    padding: 6px 9px;

    border-radius: 6px;

    background: rgba(53,211,154,0.08);

    border: 1px solid rgba(53,211,154,0.15);

    color: #4DD9A1;

    font-size: 9px;
    font-weight: 700;

    letter-spacing: 0.8px;
}

.report-content {
    padding: 30px 34px;
}

.report-content h1,
.report-content h2,
.report-content h3 {
    font-family: 'Space Grotesk', sans-serif;

    color: #F4F7FA;
}

.report-content h1 {
    font-size: 28px;
}

.report-content h2 {
    font-size: 21px;

    margin-top: 30px;

    padding-bottom: 8px;

    border-bottom: 1px solid rgba(255,255,255,0.07);
}

.report-content h3 {
    font-size: 16px;
}

.report-content p,
.report-content li {
    color: #AAB6C6;

    font-size: 14px;

    line-height: 1.75;
}

.report-content strong {
    color: #E8EEF6;
}

.report-content blockquote {
    border-left: 3px solid #2779FF;

    background: rgba(39,121,255,0.055);

    padding: 12px 16px;

    color: #AAB8CA;
}

.report-content code {
    background: #111B29;

    color: #7FC3FF;

    padding: 2px 6px;

    border-radius: 5px;
}


/* =========================================================
   SOURCE CARDS
   ========================================================= */

.source-card {
    padding: 15px 17px;

    border-radius: 11px;

    background: #0D141F;

    border: 1px solid #1D2938;

    margin-bottom: 9px;

    transition: all 0.2s ease;
}

.source-card:hover {
    border-color: #285A91;

    transform: translateX(2px);
}

.source-title {
    color: #DCE4EE;

    font-size: 13px;
    font-weight: 600;

    margin-bottom: 6px;
}

.source-url {
    color: #579BEA;

    font-size: 11px;

    word-break: break-all;
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    border-color: rgba(255,255,255,0.07) !important;
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 10px !important;
}


/* =========================================================
   STATUS COMPONENT
   ========================================================= */

div[data-testid="stStatusWidget"] {
    background: #0D141F !important;

    border: 1px solid #1D2938 !important;

    border-radius: 14px !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    margin-top: 45px;

    padding-top: 22px;

    border-top: 1px solid rgba(255,255,255,0.06);

    color: #475467;

    font-size: 11px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">◈</div>
            <div class="sidebar-brand-name">Research Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Research Configuration</div>',
        unsafe_allow_html=True,
    )

    research_depth = st.selectbox(
        "Research depth",
        ["Quick", "Standard", "Deep"],
        index=1,
        label_visibility="collapsed",
    )

    depth_info = {
        "Quick": "Fast exploratory research with a compact evidence set.",
        "Standard": "Balanced investigation across multiple source categories.",
        "Deep": "Broader evidence collection for complex questions.",
    }

    st.caption(depth_info[research_depth])

    st.markdown(
        '<div class="sidebar-section">Research Sources</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="line-height:2.1;color:#8794A7;font-size:12px;">
        ◉ Web &nbsp;·&nbsp; Current information<br>
        ◉ Academic &nbsp;·&nbsp; Scholarly literature<br>
        ◉ Industry &nbsp;·&nbsp; Companies & market evidence<br>
        ◉ Verification &nbsp;·&nbsp; Claim checking
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">Agent Team</div>',
        unsafe_allow_html=True,
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
        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:9px;
                margin:8px 0;
                color:#7F8DA1;
                font-size:11px;
            ">
                <span style="
                    width:20px;
                    height:20px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border-radius:6px;
                    background:#111A27;
                    color:#5D9FEF;
                    font-size:9px;
                    font-weight:700;
                ">{i}</span>
                {agent}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="sidebar-section">System</div>',
        unsafe_allow_html=True,
    )

    groq_ready = bool(os.getenv("GROQ_API_KEY"))
    tavily_ready = bool(os.getenv("TAVILY_API_KEY"))

    groq_status = "Connected" if groq_ready else "Missing"
    tavily_status = "Connected" if tavily_ready else "Missing"

    st.markdown(
        f"""
        <div style="
            padding:12px;
            border-radius:10px;
            background:#0D141F;
            border:1px solid #1D2938;
        ">
            <div style="
                display:flex;
                justify-content:space-between;
                margin-bottom:8px;
                color:#8794A7;
                font-size:11px;
            ">
                <span>LLM Service</span>
                <span style="color:{'#42D69C' if groq_ready else '#F97066'};">
                    {groq_status}
                </span>
            </div>

            <div style="
                display:flex;
                justify-content:space-between;
                color:#8794A7;
                font-size:11px;
            ">
                <span>Web Search</span>
                <span style="color:{'#42D69C' if tavily_ready else '#F97066'};">
                    {tavily_status}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
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
            <div class="meta-pill">7 Specialized Agents</div>
            <div class="meta-pill">Multi-Source Research</div>
            <div class="meta-pill">Evidence Verification</div>
            <div class="meta-pill">Structured Reports</div>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# RESEARCH QUESTION
# ============================================================

st.markdown(
    '<div class="section-label">01 · Investigation</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">What do you want to investigate?</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="input-shell"><div class="input-inner">', unsafe_allow_html=True)

question = st.text_area(
    "Research question",
    placeholder=(
        "Ask a complex question...\n\n"
        "Example: What are the major opportunities, risks and "
        "market trends for AI-powered cybersecurity platforms?"
    ),
    height=155,
    label_visibility="collapsed",
)

st.markdown("</div></div>", unsafe_allow_html=True)


# ============================================================
# MODE CARDS
# ============================================================

st.markdown(
    '<div class="section-label">02 · Research Depth</div>',
    unsafe_allow_html=True,
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
        "Web, academic and industry evidence.",
    ),
    (
        "Deep",
        "Extended investigation",
        "Broader evidence for complex questions.",
    ),
]

for col, (name, subtitle, description) in zip(mode_cols, mode_data):

    active = name == research_depth

    with col:
        st.markdown(
            f"""
            <div class="mode-card {'active' if active else ''}">
                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">
                    <div>
                        <div class="mode-name">{name}</div>
                        <div style="
                            color:#579BEA;
                            font-size:10px;
                            margin-top:3px;
                            font-weight:600;
                        ">
                            {subtitle}
                        </div>
                    </div>

                    <div style="
                        width:8px;
                        height:8px;
                        border-radius:50%;
                        background:{'#4DD9A1' if active else '#273447'};
                    "></div>
                </div>

                <div class="mode-description">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# START BUTTON
# ============================================================

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

start_research = st.button(
    "◈   Start Intelligence Research",
    type="primary",
    use_container_width=True,
)


# ============================================================
# PIPELINE
# ============================================================

st.markdown(
    '<div class="section-label">03 · Agent Architecture</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Seven agents. One research workflow.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pipeline-container">

        <div class="pipeline">

            <div class="pipeline-node">
                <div class="pipeline-icon">⌁</div>
                <div class="pipeline-name">Research<br>Planner</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">◉</div>
                <div class="pipeline-name">Web<br>Researcher</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">◇</div>
                <div class="pipeline-name">Academic<br>Researcher</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">▣</div>
                <div class="pipeline-name">Industry<br>Researcher</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">◎</div>
                <div class="pipeline-name">Evidence<br>Analyst</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">✓</div>
                <div class="pipeline-name">Fact<br>Checker</div>
            </div>

            <div class="pipeline-arrow">→</div>

            <div class="pipeline-node">
                <div class="pipeline-icon">✦</div>
                <div class="pipeline-name">Research<br>Synthesizer</div>
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# EXECUTION
# ============================================================

if start_research:

    if not question.strip():
        st.warning("Enter a research question before starting the investigation.")
        st.stop()

    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is not configured in Streamlit Secrets.")
        st.stop()

    if not os.getenv("TAVILY_API_KEY"):
        st.warning(
            "TAVILY_API_KEY is not configured. Web and industry research may be limited."
        )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-label">04 · Live Workflow</div>',
        unsafe_allow_html=True,
    )

    status_placeholder = st.empty()

    with status_placeholder.container():

        st.markdown(
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
                    <div class="agent-state">Planning</div>
                </div>

                <div class="agent-row">
                    <div class="agent-number">02</div>
                    <div class="agent-name">Web Researcher</div>
                    <div class="agent-state">Gathering evidence</div>
                </div>

                <div class="agent-row">
                    <div class="agent-number">03</div>
                    <div class="agent-name">Academic Researcher</div>
                    <div class="agent-state">Searching literature</div>
                </div>

                <div class="agent-row">
                    <div class="agent-number">04</div>
                    <div class="agent-name">Industry Researcher</div>
                    <div class="agent-state">Analyzing industry</div>
                </div>

                <div class="agent-row">
                    <div class="agent-number">05</div>
                    <div class="agent-name">Evidence Analyst</div>
                    <div class="agent-state">Comparing evidence</div>
                </div>

                <div class="agent-row">
                    <div class="agent-number">06</div>
                    <div class="agent-name">Fact Checker</div>
                    <div class="agent-state">Verifying claims</div>
                </div>

                <div class="agent-row">
                    <div class="agent-number">07</div>
                    <div class="agent-name">Research Synthesizer</div>
                    <div class="agent-state">Preparing report</div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    progress = st.status(
        "Agents are conducting the investigation...",
        expanded=False,
    )

    try:

        with progress:

            st.write("Research Planner is structuring the investigation.")
            st.write("Research agents are gathering evidence.")
            st.write("Evidence Analyst is comparing findings.")
            st.write("Fact Checker is validating important claims.")
            st.write("Research Synthesizer is preparing the final report.")

            research_crew = ResearchCrew()

            result = research_crew.run(
                question=question.strip(),
                depth=research_depth,
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

        st.markdown(
            '<div class="section-label">05 · Intelligence Report</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="report-shell">

                <div class="report-header">

                    <div class="report-header-title">

                        <div class="report-mark">
                            ✦
                        </div>

                        Research Intelligence Report

                    </div>

                    <div class="report-badge">
                        VERIFIED WORKFLOW
                    </div>

                </div>

                <div class="report-content">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(report)

        st.markdown(
            """
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # SOURCES
        # ----------------------------------------------------

        sources = extract_sources(report)

        if sources:

            st.markdown(
                '<div class="section-label">06 · Evidence Base</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div class="section-title">Research Sources</div>',
                unsafe_allow_html=True,
            )

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
                "The research workflow reached the current Groq token-per-minute limit."
            )

            st.info(
                "Try Quick research after the current rate-limit window resets."
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

st.markdown(
    """
    <div class="footer">
        Research Intelligence · Multi-Agent Research System
        <br>
        AI-generated research should be verified against cited sources
        before high-stakes use.
    </div>
    """,
    unsafe_allow_html=True,
)
