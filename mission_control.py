import os
import streamlit as st

# Safe import for Gemini SDK
try:
    import google.generativeai as genai

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="MISSION CONTROL // AI COMMAND CENTER",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "active_mission" not in st.session_state:
    st.session_state.active_mission = "None Initialized"
if "mission_idea" not in st.session_state:
    st.session_state.mission_idea = ""
if "feasibility_score" not in st.session_state:
    st.session_state.feasibility_score = "N/A"
if "mission_status" not in st.session_state:
    st.session_state.mission_status = "Standby"
if "scanner_result" not in st.session_state:
    st.session_state.scanner_result = None
if "intelligence_result" not in st.session_state:
    st.session_state.intelligence_result = None
if "explainer_result" not in st.session_state:
    st.session_state.explainer_result = None
if "prompt_lab_result" not in st.session_state:
    st.session_state.prompt_lab_result = None
if "research_result" not in st.session_state:
    st.session_state.research_result = None
if "radar_result" not in st.session_state:
    st.session_state.radar_result = None
if "nav_override" not in st.session_state:
    st.session_state.nav_override = None


# ==========================================
# 3. CENTRALIZED AI CORE FUNCTION
# ==========================================
def ask_ai(prompt_text):
    """Centralized AI helper function to communicate with Gemini API safely."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]

    if not api_key:
        return (
            "ERROR_MISSING_API_KEY",
            "SYSTEM ALERT: AI CORE CONNECTION FAILED. Please configure your GEMINI_API_KEY in your .streamlit/secrets.toml file.",
        )

    if not GEMINI_AVAILABLE:
        return (
            "ERROR_MISSING_PACKAGE",
            "SYSTEM ALERT: google-generativeai package is not installed. Run 'pip install google-generativeai'.",
        )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt_text)
        return "SUCCESS", response.text
    except Exception as e:
        return (
            "ERROR_API_FAILURE",
            f"SYSTEM ALERT: AI CORE TRANSMISSION FAILED.\nDetails: {str(e)}",
        )


# ==========================================
# 4. CUSTOM CYBERPUNK HUD & GRID STYLING
# ==========================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #030712 !important;
        background-image: 
            linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
        background-size: 35px 35px;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(6, 182, 212, 0.2);
    }

    @keyframes pulse-glow {
        0% { box-shadow: 0 0 5px rgba(6, 182, 212, 0.2), inset 0 0 5px rgba(6, 182, 212, 0.1); }
        50% { box-shadow: 0 0 25px rgba(6, 182, 212, 0.6), inset 0 0 15px rgba(6, 182, 212, 0.3); }
        100% { box-shadow: 0 0 5px rgba(6, 182, 212, 0.2), inset 0 0 5px rgba(6, 182, 212, 0.1); }
    }

    @keyframes live-blink {
        0% { opacity: 0.3; }
        50% { opacity: 1; }
        100% { opacity: 0.3; }
    }

    .hero-title {
        font-family: 'Courier New', monospace;
        color: #06b6d4;
        text-shadow: 0 0 12px rgba(6, 182, 212, 0.6);
        font-weight: bold;
        letter-spacing: 2px;
    }

    .system-badge {
        font-family: 'Courier New', monospace;
        background-color: rgba(6, 182, 212, 0.1);
        border: 1px solid #06b6d4;
        color: #22d3ee;
        padding: 6px 14px;
        border-radius: 4px;
        font-size: 0.85rem;
        display: inline-block;
        animation: pulse-glow 3s infinite ease-in-out;
    }

    .live-dot {
        color: #22c55e;
        animation: live-blink 2s infinite ease-in-out;
    }

    .hud-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(3, 7, 18, 0.98) 100%);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .hud-card:hover {
        border-color: rgba(6, 182, 212, 0.8);
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.35);
        transform: translateY(-2px);
    }

    .hud-card-title {
        font-family: 'Courier New', monospace;
        color: #22d3ee;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }

    .hud-card-desc {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 0px;
        line-height: 1.4;
    }

    .sidebar-status {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        padding: 12px;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 5. MODULE RENDERING FUNCTIONS
# ==========================================


def render_dashboard():
    """Renders the main Mission Control command center home screen with interactive HUD buttons."""
    st.markdown(
        "<h1 class='hero-title'>MISSION CONTROL</h1>", unsafe_allow_html=True
    )
    st.markdown("### AI VIBE-CODING COMMAND CENTER // V1.0 RC")
    st.markdown(
        "<div class='system-badge'><span class='live-dot'>[+]</span> SYSTEM ONLINE — ALL SUBROUTINES NOMINAL</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #94a3b8; font-family: monospace;'>SELECT AN INTEL MODULE TO INITIALIZE SUBROUTINE:</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="font-family: 'Courier New', monospace; color: #22d3ee; font-weight: bold; margin-bottom: 4px;">01 // IDEA SCANNER</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Analyze project feasibility, complexity metrics, and potential bottlenecks.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("INITIALIZE: IDEA SCANNER", use_container_width=True):
            st.session_state.nav_override = "01 — Idea Scanner"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="font-family: 'Courier New', monospace; color: #22d3ee; font-weight: bold; margin-bottom: 4px;">03 // PROJECT EXPLAINER</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Break down your architecture across beginner, technical, and viva levels.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("INITIALIZE: PROJECT EXPLAINER", use_container_width=True):
            st.session_state.nav_override = "03 — Project Explainer"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="font-family: 'Courier New', monospace; color: #22d3ee; font-weight: bold; margin-bottom: 4px;">05 // RESEARCH LAB</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Retrieve peer-reviewed academic papers and precise APA citations.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("INITIALIZE: RESEARCH LAB", use_container_width=True):
            st.session_state.nav_override = "05 — Research Lab"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div style="font-family: 'Courier New', monospace; color: #22d3ee; font-weight: bold; margin-bottom: 4px;">02 // PROJECT INTELLIGENCE</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Generate comprehensive blueprints, data flows, and architecture maps.</div>
            """,
            unsafe_allow_html=True,
        )
        if (
            st.button(
                "INITIALIZE: PROJECT INTELLIGENCE", use_container_width=True
            )
        ):
            st.session_state.nav_override = "02 — Project Intelligence"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="font-family: 'Courier New', monospace; color: #22d3ee; font-weight: bold; margin-bottom: 4px;">04 // PROMPT LAB</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Synthesize production-grade vibe-coding prompts for Cursor or Claude.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("INITIALIZE: PROMPT LAB", use_container_width=True):
            st.session_state.nav_override = "04 — Prompt Lab"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="font-family: 'Courier New', monospace; color: #22d3ee; font-weight: bold; margin-bottom: 4px;">06 // AI RADAR</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Scan live tech trends, coding signals, and future-proofing telemetry.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("INITIALIZE: AI RADAR", use_container_width=True):
            st.session_state.nav_override = "06 — AI Radar"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hud-card" style="border-color: rgba(6, 182, 212, 0.5);">
            <div class="hud-card-title" style="color: #38bdf8;">ACTIVE MISSION TELEMETRY SNAPSHOT</div>
            <div class="hud-card-desc">
                <b>CURRENT PROJECT:</b> {st.session_state.active_mission}<br>
                <b>STATUS:</b> {st.session_state.mission_status}<br>
                <b>FEASIBILITY:</b> {st.session_state.feasibility_score}<br>
                <b>IDEA SEED:</b> {st.session_state.mission_idea if st.session_state.mission_idea else "Awaiting telemetry input..."}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if (
        st.session_state.scanner_result
        or st.session_state.intelligence_result
        or st.session_state.prompt_lab_result
    ):
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='color: #22d3ee; font-family: monospace;'>MISSION CONTROL EXPORT</h3>",
            unsafe_allow_html=True,
        )
        st.write(
            "Export all generated telemetry and intelligence reports into a single compiled Markdown document."
        )

        export_markdown = f"""# MISSION CONTROL // INTELLIGENCE EXPORT REPORT
**Active Mission:** {st.session_state.active_mission}
**Mission Status:** {st.session_state.mission_status}
**Idea Seed:** {st.session_state.mission_idea}
---
"""
        if st.session_state.scanner_result:
            export_markdown += f"\n## 01 // IDEA SCANNER REPORT\n{st.session_state.scanner_result}\n\n---\n"
        if st.session_state.intelligence_result:
            export_markdown += f"\n## 02 // PROJECT INTELLIGENCE BLUEPRINT\n{st.session_state.intelligence_result}\n\n---\n"
        if st.session_state.explainer_result:
            export_markdown += f"\n## 03 // PROJECT EXPLAINER REPORT\n{st.session_state.explainer_result}\n\n---\n"
        if st.session_state.prompt_lab_result:
            export_markdown += f"\n## 04 // MASTER PROMPT LAB\n{st.session_state.prompt_lab_result}\n\n---\n"
        if st.session_state.research_result:
            export_markdown += f"\n## 05 // RESEARCH LAB LITERATURE\n{st.session_state.research_result}\n\n---\n"
        if st.session_state.radar_result:
            export_markdown += f"\n## 06 // AI RADAR BRIEFING\n{st.session_state.radar_result}\n\n---\n"

        st.download_button(
            label="DOWNLOAD COMPILED MISSION REPORT (.MD)",
            data=export_markdown,
            file_name="mission_control_report.md",
            mime="text/markdown",
        )


def render_idea_scanner():
    st.markdown("<h1 class='hero-title'>01 // IDEA SCANNER</h1>", unsafe_allow_html=True)
    st.write(
        "Analyze whether your project idea is feasible using AI telemetry."
    )
    st.markdown("---")

    user_idea = st.text_area(
        "ENTER PROJECT CONCEPT:",
        value=st.session_state.mission_idea,
        placeholder="e.g., An AI study habit analyzer that tracks focus and recommends breaks.",
    )

    if st.button("INITIALIZE IDEA SCAN"):
        if not user_idea.strip():
            st.warning("Please enter a valid project concept first.")
            return

        with st.spinner(
            "SCANNING TELEMETRY // CONSULTING GEMINI AI CORE..."
        ):
            prompt = f"""
            You are an expert AI Product Manager and senior technical architect. Analyze the following project idea for an MVP build:
            Project Idea: "{user_idea}"

            Provide a rigorous, structured evaluation covering exactly these headers:
            1. PROJECT VERDICT (Choose one: HIGHLY FEASIBLE, FEASIBLE, FEASIBLE WITH LIMITATIONS, DIFFICULT, NOT CURRENTLY FEASIBLE)
            2. FEASIBILITY SCORE (Out of 100, e.g., 85 / 100)
            3. COMPLEXITY (Use symbol scale, e.g., HIGH / MEDIUM / LOW)
            4. ESTIMATED BUILD DIFFICULTY (Beginner / Intermediate / Advanced)
            5. REQUIRED TECHNOLOGIES (Bullet points)
            6. CORE FEATURES (Bullet points)
            7. POTENTIAL CHALLENGES (Realistic technical problems)
            8. SIMPLER MVP (How to build a simpler first version)
            9. FINAL RECOMMENDATION (Honest advice on whether to build it)

            Keep the tone professional, technical, and realistic. Use Markdown formatting.
            """

            status, result = ask_ai(prompt)

            if status == "SUCCESS":
                st.session_state.mission_idea = user_idea
                st.session_state.active_mission = (
                    user_idea[:30] + "..."
                    if len(user_idea) > 30
                    else user_idea
                )
                st.session_state.mission_status = "Idea Scanned & Verified"
                st.session_state.feasibility_score = "Analyzed by AI"
                st.session_state.scanner_result = result
                st.success("Telemetry scan complete. Report generated below.")
            else:
                st.markdown(
                    f"""
                    <div class="hud-card" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.05);">
                        <div class="hud-card-title" style="color: #ef4444;">SYSTEM ALERT</div>
                        <div class="hud-card-desc" style="color: #f87171;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.session_state.scanner_result:
        st.markdown("---")
        st.markdown(
            "<h3 style='color: #22d3ee; font-family: monospace;'>SCANNER EVALUATION REPORT</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='hud-card'>{st.session_state.scanner_result}</div>",
            unsafe_allow_html=True,
        )


def render_project_intelligence():
    st.markdown(
        "<h1 class='hero-title'>02 // PROJECT INTELLIGENCE</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "Generate a comprehensive architectural blueprint for your active mission."
    )
    st.markdown("---")

    default_target = (
        st.session_state.mission_idea
        if st.session_state.mission_idea
        else ""
    )
    target_project = st.text_input(
        "MISSION TARGET / PROJECT NAME:",
        value=default_target,
        placeholder="e.g., AI study habit analyzer",
    )

    if st.button("GENERATE BLUEPRINT"):
        if not target_project.strip():
            st.warning(
                "Please enter a mission target or initialize an idea in Module 01 first."
            )
            return

        with st.spinner(
            "COMPILING BLUEPRINT TELEMETRY // CONSULTING ARCHITECT AI..."
        ):
            prompt = f"""
            You are a Principal Software Architect and AI Product Manager. Generate a comprehensive technical project blueprint for the following concept:
            Project: "{target_project}"

            Provide a rigorous, structured technical blueprint covering exactly these headers:
            1. EXECUTIVE ARCHITECTURE OVERVIEW
            2. SYSTEM DATA FLOW (Step-by-step user journey)
            3. RECOMMENDED TECH STACK (Frontend, Backend, Database, AI/ML Services)
            4. DATABASE SCHEMA DESIGN (Key tables/collections and relationships)
            5. CORE API ENDPOINTS (Method, Route, and Purpose)
            6. SECURITY & DATA PRIVACY CONSIDERATIONS
            7. STEP-BY-STEP VIBE-CODING IMPLEMENTATION ROADMAP

            Keep the tone professional, technical, and precise. Use Markdown formatting.
            """

            status, result = ask_ai(prompt)

            if status == "SUCCESS":
                st.session_state.mission_idea = target_project
                st.session_state.active_mission = (
                    target_project[:30] + "..."
                    if len(target_project) > 30
                    else target_project
                )
                st.session_state.mission_status = "Blueprint Generated"
                st.session_state.intelligence_result = result
                st.success(
                    "Blueprint compilation successful. Telemetry synced."
                )
            else:
                st.markdown(
                    f"""
                    <div class="hud-card" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.05);">
                        <div class="hud-card-title" style="color: #ef4444;">SYSTEM ALERT</div>
                        <div class="hud-card-desc" style="color: #f87171;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.session_state.intelligence_result:
        st.markdown("---")
        st.markdown(
            "<h3 style='color: #22d3ee; font-family: monospace;'>ARCHITECTURAL BLUEPRINT REPORT</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='hud-card'>{st.session_state.intelligence_result}</div>",
            unsafe_allow_html=True,
        )


def render_project_explainer():
    st.markdown(
        "<h1 class='hero-title'>03 // PROJECT EXPLAINER</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "Break down your active mission for beginners, technical teams, and viva/interview defense."
    )
    st.markdown("---")

    default_target = (
        st.session_state.mission_idea
        if st.session_state.mission_idea
        else ""
    )
    target_project = st.text_input(
        "MISSION TARGET TO EXPLAIN:",
        value=default_target,
        placeholder="e.g., AI study habit analyzer",
    )

    if st.button("GENERATE EXPLANATIONS"):
        if not target_project.strip():
            st.warning("Please specify a project target first.")
            return

        with st.spinner(
            "SYNTHESIZING MULTI-TIER EXPLANATIONS // CONSULTING EXPLAINER AI..."
        ):
            prompt = f"""
            You are a master communicator, tech educator, and senior software engineer. Provide multi-tier explanations for the following project:
            Project: "{target_project}"

            Provide a structured breakdown covering exactly these 3 sections:
            1. ELI5 / BEGINNER EXPLANATION (Explain it simply using a relatable everyday analogy, zero jargon)
            2. TECHNICAL ARCHITECTURE EXPLANATION (Explain how the backend, frontend, database, and AI models interact under the hood)
            3. VIVA & INTERVIEW DEFENSE (List 3 tough questions an examiner or technical interviewer might ask about this project, along with strong, concise answers)

            Keep the tone professional, educational, and engaging. Use Markdown formatting.
            """

            status, result = ask_ai(prompt)

            if status == "SUCCESS":
                st.session_state.mission_idea = target_project
                st.session_state.active_mission = (
                    target_project[:30] + "..."
                    if len(target_project) > 30
                    else target_project
                )
                st.session_state.mission_status = "Explanations Compiled"
                st.session_state.explainer_result = result
                st.success("Multi-tier explanation matrix generated.")
            else:
                st.markdown(
                    f"""
                    <div class="hud-card" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.05);">
                        <div class="hud-card-title" style="color: #ef4444;">SYSTEM ALERT</div>
                        <div class="hud-card-desc" style="color: #f87171;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.session_state.explainer_result:
        st.markdown("---")
        st.markdown(
            "<h3 style='color: #22d3ee; font-family: monospace;'>MULTI-TIER EXPLANATION REPORT</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='hud-card'>{st.session_state.explainer_result}</div>",
            unsafe_allow_html=True,
        )


def render_prompt_lab():
    st.markdown(
        "<h1 class='hero-title'>04 // PROMPT LAB</h1>", unsafe_allow_html=True
    )
    st.write(
        "Synthesize production-grade, highly structured vibe-coding prompts for Cursor, Claude, or ChatGPT."
    )
    st.markdown("---")

    default_target = (
        st.session_state.mission_idea
        if st.session_state.mission_idea
        else ""
    )
    target_project = st.text_input(
        "MISSION TARGET FOR PROMPT SYNTHESIS:",
        value=default_target,
        placeholder="e.g., AI study habit analyzer",
    )

    ai_tool = st.selectbox(
        "TARGET VIBE-CODING ASSISTANT:",
        [
            "Cursor (AI Code Editor)",
            "Claude 3.5 Sonnet",
            "ChatGPT (GPT-4o)",
            "General LLM",
        ],
    )

    if st.button("SYNTHESIZE MASTER PROMPT"):
        if not target_project.strip():
            st.warning("Please specify a project target first.")
            return

        with st.spinner(
            "CRAFTING PRODUCTION-GRADE PROMPT // CONSULTING PROMPT ENGINEER AI..."
        ):
            prompt = f"""
            You are an elite prompt engineer and expert vibe-coder. Create a comprehensive, production-ready master prompt for an AI assistant ({ai_tool}) to build the following application:
            Project: "{target_project}"

            Structure the generated master prompt using Markdown so the user can easily copy and paste it into {ai_tool}. Include:
            1. Role & Context Definition
            2. Core Objective & Requirements
            3. Technical Stack Constraints
            4. Step-by-Step Implementation Instructions for the AI
            5. Expected Output Format

            Make the prompt extremely detailed, precise, and structured so the AI assistant builds the app correctly on the first try.
            """

            status, result = ask_ai(prompt)

            if status == "SUCCESS":
                st.session_state.mission_idea = target_project
                st.session_state.active_mission = (
                    target_project[:30] + "..."
                    if len(target_project) > 30
                    else target_project
                )
                st.session_state.mission_status = "Master Prompt Synthesized"
                st.session_state.prompt_lab_result = result
                st.success("Master vibe-coding prompt synthesized successfully.")
            else:
                st.markdown(
                    f"""
                    <div class="hud-card" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.05);">
                        <div class="hud-card-title" style="color: #ef4444;">SYSTEM ALERT</div>
                        <div class="hud-card-desc" style="color: #f87171;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.session_state.prompt_lab_result:
        st.markdown("---")
        st.markdown(
            "<h3 style='color: #22d3ee; font-family: monospace;'>SYNTHESIZED MASTER PROMPT</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='hud-card'>{st.session_state.prompt_lab_result}</div>",
            unsafe_allow_html=True,
        )


def render_research_lab():
    st.markdown(
        "<h1 class='hero-title'>05 // RESEARCH LAB</h1>", unsafe_allow_html=True
    )
    st.write(
        "Retrieve peer-reviewed academic papers, relevance scores, and precise APA citations for your research domain."
    )
    st.markdown("---")

    default_query = (
        st.session_state.mission_idea
        if st.session_state.mission_idea
        else ""
    )
    research_query = st.text_input(
        "RESEARCH TOPIC OR DOMAIN QUERY:",
        value=default_query,
        placeholder="e.g., Human-AI collaboration in productivity tracking systems",
    )

    if st.button("RETRIEVE RESEARCH PAPERS"):
        if not research_query.strip():
            st.warning("Please enter a research topic or query.")
            return

        with st.spinner(
            "QUERIED ACADEMIC DATABASES // CONSULTING RESEARCH AI..."
        ):
            prompt = f"""
            You are an expert academic researcher and literature reviewer. Provide 3 highly relevant peer-reviewed or conference research papers related to the following topic:
            Topic: "{research_query}"

            For each paper, provide:
            1. Paper Title & Publication Year
            2. Relevance Score (out of 100)
            3. Summary of Core Methodology & Findings (2-3 sentences)
            4. Precise APA Citation

            Keep the tone scholarly, rigorous, and professional. Use Markdown formatting.
            """

            status, result = ask_ai(prompt)

            if status == "SUCCESS":
                st.session_state.mission_idea = research_query
                st.session_state.active_mission = (
                    research_query[:30] + "..."
                    if len(research_query) > 30
                    else research_query
                )
                st.session_state.mission_status = "Research Papers Retrieved"
                st.session_state.research_result = result
                st.success(
                    "Academic literature database queried successfully."
                )
            else:
                st.markdown(
                    f"""
                    <div class="hud-card" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.05);">
                        <div class="hud-card-title" style="color: #ef4444;">SYSTEM ALERT</div>
                        <div class="hud-card-desc" style="color: #f87171;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.session_state.research_result:
        st.markdown("---")
        st.markdown(
            "<h3 style='color: #22d3ee; font-family: monospace;'>RETRIEVED LITERATURE REPORT</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='hud-card'>{st.session_state.research_result}</div>",
            unsafe_allow_html=True,
        )


def render_ai_radar():
    st.markdown(
        "<h1 class='hero-title'>06 // AI RADAR</h1>", unsafe_allow_html=True
    )
    st.write(
        "Scan live tech trends, AI coding signals, framework momentum, and future-proofing telemetry."
    )
    st.markdown("---")

    radar_sector = st.selectbox(
        "SELECT RADAR INTEL SECTOR:",
        [
            "AI Coding Assistants & Vibe Tools (Cursor, v0, Copilot)",
            "Frontend & Rapid UI Frameworks (Streamlit, React, Next.js)",
            "Backend & Agentic APIs (FastAPI, LangChain, Gemini API)",
            "Full-Stack Ecosystem Overview & Emerging Tech",
        ],
    )

    if st.button("SCAN RADAR TELEMETRY"):
        with st.spinner(
            "SCANNING GLOBAL TECH RADAR // CONSULTING TREND ANALYZER AI..."
        ):
            prompt = f"""
            You are a Principal Tech Trend Analyst and Futurist. Generate an intelligence briefing and Tech Radar report for the following sector:
            Sector: "{radar_sector}"

            Provide a structured report using these exact headers:
            1. EXECUTIVE MOMENTUM OVERVIEW (Current state of adoption and velocity)
            2. ADOPT / TRIAL / ASSESS / HOLD RECOMMENDATIONS (Categorize key tools or frameworks into these 4 ThoughtWorks-style radar rings)
            3. KEY BREAKTHROUGHS & CAPABILITIES (What's new or changing rapidly)
            4. STRATEGIC ADVICE FOR VIBE-CODERS (How developers should leverage this sector right now)

            Keep the tone professional, futuristic, and actionable. Use Markdown formatting.
            """

            status, result = ask_ai(prompt)

            if status == "SUCCESS":
                st.session_state.mission_status = "AI Radar Scanned"
                st.session_state.radar_result = result
                st.success("Radar telemetry scan completed successfully.")
            else:
                st.markdown(
                    f"""
                    <div class="hud-card" style="border-color: #ef4444; background: rgba(239, 68, 68, 0.05);">
                        <div class="hud-card-title" style="color: #ef4444;">SYSTEM ALERT</div>
                        <div class="hud-card-desc" style="color: #f87171;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    if st.session_state.radar_result:
        st.markdown("---")
        st.markdown(
            "<h3 style='color: #22d3ee; font-family: monospace;'>TECH RADAR INTELLIGENCE BRIEFING</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='hud-card'>{st.session_state.radar_result}</div>",
            unsafe_allow_html=True,
        )


# ==========================================
# 6. SIDEBAR NAVIGATION & CONTROLS
# ==========================================
def render_sidebar():
    with st.sidebar:
        st.markdown(
            "<h2 style='color: #06b6d4; font-family: monospace;'>COMMAND</h2>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="sidebar-status">
                <b>SYSTEM STATUS:</b> <span style="color: #22c55e;" class="live-dot">[+] ONLINE</span><br>
                <b>ACTIVE:</b> {st.session_state.active_mission[:18]}...<br>
                <b>VERSION:</b> v1.0 RC
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("### NAVIGATION")

        modules = [
            "Mission Control (Home)",
            "01 — Idea Scanner",
            "02 — Project Intelligence",
            "03 — Project Explainer",
            "04 — Prompt Lab",
            "05 — Research Lab",
            "06 — AI Radar",
        ]

        default_index = 0
        if st.session_state.get("nav_override") in modules:
            default_index = modules.index(st.session_state.nav_override)
            st.session_state.nav_override = None  # Clear override after reading

        nav_choice = st.radio(
            "Select Module", modules, index=default_index, label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown(
            "<p style='font-size: 0.75rem; color: #64748b;'>MISSION CONTROL V1.0 // FULLY OPERATIONAL</p>",
            unsafe_allow_html=True,
        )

        return nav_choice


# ==========================================
# 7. MAIN APP ROUTER
# ==========================================
def main():
    selected_module = render_sidebar()

    if selected_module == "Mission Control (Home)":
        render_dashboard()
    elif selected_module == "01 — Idea Scanner":
        render_idea_scanner()
    elif selected_module == "02 — Project Intelligence":
        render_project_intelligence()
    elif selected_module == "03 — Project Explainer":
        render_project_explainer()
    elif selected_module == "04 — Prompt Lab":
        render_prompt_lab()
    elif selected_module == "05 — Research Lab":
        render_research_lab()
    elif selected_module == "06 — AI Radar":
        render_ai_radar()


if __name__ == "__main__":
    main()