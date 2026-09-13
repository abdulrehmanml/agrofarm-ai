"""
AgroFarm AI - Farmer-Friendly Streamlit Interface
====================================================
UI layer connected to the OOP-based src/ backend engines.

RUN:
    streamlit run app.py
"""

import csv
import html
import os
import time
from datetime import datetime

import streamlit as st

from src.rag_engine import RAGEngine
from src.weather_engine import WeatherEngine
from src.llm_engine import LLMEngine
from src.config import GEMINI_API_KEY

# Initialize our OOP backend engines once and cache them
@st.cache_resource
def init_system():
    return RAGEngine(), LLMEngine(), WeatherEngine()

rag, llm, weather = init_system()

DECISION_LOG_PATH = os.path.join(os.path.dirname(__file__), "data", "decision_log.csv")

st.set_page_config(
    page_title="AgriSense AI | Smart Farm Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Styling - farmer-first, clean, mobile-friendly Streamlit UI
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Main page */
        .stApp {
            background: linear-gradient(180deg, #f7fbf7 0%, #ffffff 38%, #f8faf8 100%);
        }

        /* Streamlit Top Header/Navigation Bar */
        [data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.82) !important;
        }

        /* Dark green high-contrast text and icons inside top header */
        [data-testid="stHeader"] *,
        [data-testid="stHeader"] button,
        [data-testid="stHeader"] button *,
        [data-testid="stHeader"] span,
        [data-testid="stHeader"] div,
        [data-testid="stHeader"] svg,
        [data-testid="stHeader"] a {
            color: #173d2b !important;
            fill: #173d2b !important;
            stroke: #173d2b !important;
            font-weight: 700 !important;
        }

        /* Hover state for buttons in the header */
        [data-testid="stHeader"] button:hover {
            background-color: rgba(23, 61, 43, 0.1) !important;
            border-radius: 8px !important;
        }

        .block-container {
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Sidebar Base */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #173d2b 0%, #102f22 100%) !important;
        }

        /* High-contrast Sidebar Text & Markdown Elements */
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] li,
        section[data-testid="stSidebar"] strong,
        section[data-testid="stSidebar"] label {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] small {
            color: #d1e8da !important;
        }

        /* High-contrast Sidebar Info Callout Box (st.sidebar.info) */
        section[data-testid="stSidebar"] [data-testid="stAlert"] {
            background-color: #0d261a !important;
            border: 1px solid #3ca870 !important;
            border-left: 6px solid #4ade80 !important;
            border-radius: 12px !important;
        }

        section[data-testid="stSidebar"] [data-testid="stAlert"] [data-testid="stMarkdownContainer"],
        section[data-testid="stSidebar"] [data-testid="stAlert"] [data-testid="stMarkdownContainer"] * {
            color: #ffffff !important;
        }

        /* === Ultimate Sidebar Expander Fix === */
        section[data-testid="stSidebar"] details {
            background-color: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.22) !important;
            border-radius: 10px !important;
        }

        /* Force transparent background on header in ALL states (hover/focus/active/open) */
        section[data-testid="stSidebar"] details summary,
        section[data-testid="stSidebar"] details summary:hover,
        section[data-testid="stSidebar"] details summary:focus,
        section[data-testid="stSidebar"] details summary:active,
        section[data-testid="stSidebar"] details[open] summary {
            background-color: transparent !important;
            color: #ffffff !important;
            outline: none !important;
        }

        /* Force all inner elements (text, icons) to white in ALL states */
        section[data-testid="stSidebar"] details summary *,
        section[data-testid="stSidebar"] details summary:hover *,
        section[data-testid="stSidebar"] details summary:focus *,
        section[data-testid="stSidebar"] details summary:active * {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        /* Lock the inner body content text to white */
        section[data-testid="stSidebar"] details [data-testid="stMarkdownContainer"],
        section[data-testid="stSidebar"] details [data-testid="stMarkdownContainer"] * {
            color: #ffffff !important;
        }

        /* Sidebar Buttons */
        section[data-testid="stSidebar"] .stButton > button {
            color: #ffffff !important;
            background: rgba(255,255,255,0.12) !important;
            border-color: rgba(255,255,255,0.3) !important;
        }
        
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stButton > button span,
        section[data-testid="stSidebar"] .stButton > button div {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover,
        section[data-testid="stSidebar"] .stButton > button:focus,
        section[data-testid="stSidebar"] .stButton > button:focus-visible,
        section[data-testid="stSidebar"] .stButton > button:active {
            color: #173d2b !important;
            background: #ffffff !important;
            border-color: #ffffff !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover p,
        section[data-testid="stSidebar"] .stButton > button:hover span,
        section[data-testid="stSidebar"] .stButton > button:hover div {
            color: #173d2b !important;
        }

        /* Force Expanders & Status Containers to light styling across ALL states */
        [data-testid="stMain"] details,
        [data-testid="stMain"] details summary,
        [data-testid="stMain"] [data-testid="stStatusWidget"],
        [data-testid="stMain"] [data-testid="stStatusWidget"] summary {
            background-color: #f0fff4 !important;
            border: 1px solid #bfe3cb !important;
            border-radius: 12px !important;
        }

        /* Prevent dark background on hover, focus, active, or click */
        [data-testid="stMain"] details:hover,
        [data-testid="stMain"] details:focus,
        [data-testid="stMain"] details:active,
        [data-testid="stMain"] details summary:hover,
        [data-testid="stMain"] details summary:focus,
        [data-testid="stMain"] details summary:active,
        [data-testid="stMain"] [data-testid="stStatusWidget"]:hover,
        [data-testid="stMain"] [data-testid="stStatusWidget"]:focus,
        [data-testid="stMain"] [data-testid="stStatusWidget"]:active,
        [data-testid="stMain"] [data-testid="stStatusWidget"] summary:hover,
        [data-testid="stMain"] [data-testid="stStatusWidget"] summary:focus,
        [data-testid="stMain"] [data-testid="stStatusWidget"] summary:active {
            background-color: #e2f7ea !important;
            color: #183b29 !important;
        }

        /* Ensure all inner text & icons remain high-contrast dark green */
        [data-testid="stMain"] details *,
        [data-testid="stMain"] details summary *,
        [data-testid="stMain"] [data-testid="stStatusWidget"] *,
        [data-testid="stMain"] [data-testid="stStatusWidget"] summary * {
            color: #183b29 !important;
            fill: #183b29 !important;
            stroke: #183b29 !important;
        }

        /* Hero */
        .hero {
            padding: 1.35rem 1.5rem;
            border-radius: 22px;
            background: linear-gradient(135deg, #1f6b46 0%, #2d8b5b 55%, #6cae72 100%);
            box-shadow: 0 12px 30px rgba(31,107,70,0.18);
            margin-bottom: 1.25rem;
        }

        .hero-title {
            color: white;
            font-size: 2.15rem;
            font-weight: 800;
            margin: 0;
            line-height: 1.15;
        }

        .hero-subtitle {
            color: #effff4;
            font-size: 1.02rem;
            margin: 0.45rem 0 0;
            line-height: 1.55;
        }

        .hero-badge {
            display: inline-block;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.25);
            color: white;
            border-radius: 999px;
            padding: 0.28rem 0.7rem;
            font-size: 0.78rem;
            font-weight: 700;
            margin-top: 0.85rem;
        }

        /* Simple feature cards */
        .feature-card {
            background: white;
            border: 1px solid #e4eee7;
            border-radius: 16px;
            padding: 1rem 1.05rem;
            min-height: 112px;
            box-shadow: 0 5px 18px rgba(21, 54, 38, 0.06);
        }

        .feature-icon {
            font-size: 1.45rem;
        }

        .feature-title {
            font-weight: 750;
            color: #183b29;
            margin-top: 0.3rem;
        }

        .feature-text {
            color: #66756c;
            font-size: 0.88rem;
            line-height: 1.4;
            margin-top: 0.2rem;
        }

        /* Agent recommendation card */
        .recommendation-card {
            background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
            border: 1px solid #bfe3cb;
            border-left: 6px solid #2d8b5b;
            border-radius: 18px;
            padding: 1.2rem 1.3rem;
            box-shadow: 0 8px 24px rgba(45,139,91,0.10);
            margin: 0.75rem 0 1rem;
        }

        .recommendation-label {
            color: #2d8b5b;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .recommendation-text {
            color: #173d2b;
            font-size: 1.25rem;
            font-weight: 750;
            line-height: 1.45;
            margin-top: 0.35rem;
        }

        /* Status pills */
        .pill {
            display: inline-block;
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            font-weight: 750;
            font-size: 0.84rem;
            margin-right: 0.35rem;
        }

        .pill-high { background: #ffe7e7; color: #a42323; }
        .pill-medium { background: #fff4d6; color: #8b6400; }
        .pill-low { background: #e3f7e9; color: #21643a; }
        .pill-neutral { background: #edf2ef; color: #53645a; }

        /* Main content text */
        [data-testid="stMain"] [data-testid="stMarkdownContainer"],
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] span,
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] strong,
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] em,
        [data-testid="stMain"] [data-testid="stMarkdownContainer"] label {
            color: #183b29 !important;
        }

        [data-testid="stMain"] [data-testid="stCaptionContainer"],
        [data-testid="stMain"] [data-testid="stCaptionContainer"] * {
            color: #52665a !important;
        }

        /* Widget labels and helper text */
        [data-testid="stMain"] label,
        [data-testid="stMain"] [data-testid="stWidgetLabel"] p,
        [data-testid="stMain"] [data-testid="stWidgetLabel"] span {
            color: #183b29 !important;
        }

        /* Tabs */
        [data-testid="stMain"] button[data-baseweb="tab"],
        [data-testid="stMain"] button[data-baseweb="tab"] p,
        [data-testid="stMain"] button[data-baseweb="tab"] span {
            color: #183b29 !important;
        }

        [data-testid="stMain"] button[data-baseweb="tab"][aria-selected="true"],
        [data-testid="stMain"] button[data-baseweb="tab"][aria-selected="true"] p,
        [data-testid="stMain"] button[data-baseweb="tab"][aria-selected="true"] span {
            color: #1f6b46 !important;
            font-weight: 800 !important;
        }

        .ai-answer {
            color: #183b29 !important;
            background: #ffffff;
            border: 1px solid #e4eee7;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            line-height: 1.65;
            font-size: 1rem;
            white-space: pre-wrap;
            box-shadow: 0 4px 14px rgba(21, 54, 38, 0.05);
            margin-bottom: 1rem;
        }

        /* Section headings */
        .section-kicker {
            color: #2d8b5b;
            font-size: 0.76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.15rem;
        }

        .section-title {
            color: #173d2b;
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .helper {
            color: #66756c;
            line-height: 1.5;
        }

        /* Inputs */
        div[data-baseweb="select"] > div,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stTextInput"] input {
            border-radius: 12px;
        }

        /* Buttons in MAIN CONTENT */
        [data-testid="stMain"] .stButton > button {
            border-radius: 11px;
            font-weight: 700;
            min-height: 2.65rem;
            color: #183b29 !important;
            background: #ffffff !important;
            border: 1px solid #b8d5c1 !important;
            box-shadow: 0 2px 8px rgba(21, 54, 38, 0.06);
        }

        [data-testid="stMain"] .stButton > button p,
        [data-testid="stMain"] .stButton > button span,
        [data-testid="stMain"] .stButton > button div {
            color: #183b29 !important;
        }

        [data-testid="stMain"] .stButton > button:hover {
            background: #1f6b46 !important;
            border-color: #1f6b46 !important;
            color: #ffffff !important;
        }

        [data-testid="stMain"] .stButton > button:hover p,
        [data-testid="stMain"] .stButton > button:hover span,
        [data-testid="stMain"] .stButton > button:hover div {
            color: #ffffff !important;
        }

        [data-testid="stMain"] .stButton > button:focus,
        [data-testid="stMain"] .stButton > button:focus-visible,
        [data-testid="stMain"] .stButton > button:active,
        [data-testid="stMain"] .stButton > button[aria-pressed="true"] {
            background: #174f34 !important;
            border-color: #174f34 !important;
            color: #ffffff !important;
            outline: 2px solid #8bc59b !important;
            outline-offset: 2px;
        }

        [data-testid="stMain"] .stButton > button:focus p,
        [data-testid="stMain"] .stButton > button:focus span,
        [data-testid="stMain"] .stButton > button:focus div,
        [data-testid="stMain"] .stButton > button:focus-visible p,
        [data-testid="stMain"] .stButton > button:focus-visible span,
        [data-testid="stMain"] .stButton > button:focus-visible div,
        [data-testid="stMain"] .stButton > button:active p,
        [data-testid="stMain"] .stButton > button:active span,
        [data-testid="stMain"] .stButton > button:active div,
        [data-testid="stMain"] .stButton > button[aria-pressed="true"] p,
        [data-testid="stMain"] .stButton > button[aria-pressed="true"] span,
        [data-testid="stMain"] .stButton > button[aria-pressed="true"] div {
            color: #ffffff !important;
        }

        /* Primary buttons keep white text on green background */
        .stButton > button[kind="primary"] {
            background: #1f6b46 !important;
            border-color: #1f6b46 !important;
            color: #ffffff !important;
        }

        .stButton > button[kind="primary"] p,
        .stButton > button[kind="primary"] span,
        .stButton > button[kind="primary"] div {
            color: #ffffff !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[kind="primary"]:focus,
        .stButton > button[kind="primary"]:focus-visible,
        .stButton > button[kind="primary"]:active {
            background: #174f34 !important;
            border-color: #174f34 !important;
            color: #ffffff !important;
        }

        /* Metrics */
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e4eee7;
            border-radius: 14px;
            padding: 0.8rem;
        }

        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }

        @media (max-width: 768px) {
            .block-container { padding-top: 1rem; }
            .hero-title { font-size: 1.65rem; }
            .hero-subtitle { font-size: 0.92rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Decision log (unchanged functionality)
# ---------------------------------------------------------------------------
def log_decision(field_id, field_name, recommendation, human_decision):
    os.makedirs(os.path.dirname(DECISION_LOG_PATH), exist_ok=True)
    file_exists = os.path.isfile(DECISION_LOG_PATH)
    with open(DECISION_LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp", "field_id", "field_name", "recommendation", "human_decision"]
            )
        writer.writerow(
            [
                datetime.now().isoformat(timespec="seconds"),
                field_id,
                field_name,
                recommendation,
                human_decision,
            ]
        )


def load_decision_log():
    if not os.path.isfile(DECISION_LOG_PATH):
        return []
    with open(DECISION_LOG_PATH, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# API key
# ---------------------------------------------------------------------------
api_key = GEMINI_API_KEY
if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
    api_key = None


# ---------------------------------------------------------------------------
# Sidebar - customer-friendly by default; technical details are collapsed
# for judges/admins.
# ---------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style="text-align:center; padding:0.6rem 0 1rem;">
        <div style="font-size:2.5rem;">🌾</div>
        <div style="font-size:1.35rem; font-weight:800; color:#ffffff;">AgriSense AI</div>
        <div style="font-size:0.83rem; color:#d1e8da; margin-top:0.2rem;">
            Smart agricultural guidance
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### 👨‍🌾 Farmer Guide")
st.sidebar.markdown(
    "**1.** Ask a natural language question\n\n"
    "**2.** Select your specific field plot\n\n"
    "**3.** Review AI-generated agronomy advice\n\n"
    "**4.** Approve or reject the recommendation"
)

st.sidebar.info(
    "💡 **Data-Driven Farming.**\n\n"
    "AgriSense dynamically combines live weather telemetry, current soil moisture, and a localized agricultural knowledge base to generate highly precise recommendations."
)

st.sidebar.divider()

with st.sidebar.expander("🚀 Tech Stack & Architecture", expanded=False):
    st.markdown(
        "**Core Technologies**\n"
        "- **LLM:** Google Gemini 2.5\n"
        "- **Vector DB:** ChromaDB (Local)\n"
        "- **Frontend:** Streamlit\n"
        "- **Architecture:** Modular OOP (src folder)\n\n"
        "**Key Implementations**\n"
        "- **RAG Pipeline:** Semantic retrieval using TF-IDF & ChromaDB for context grounding.\n"
        "- **Agentic Workflow:** Merges static document knowledge with live field telemetry.\n"
        "- **Human-in-the-Loop:** Persistent decision logging and audit trails for recommendations."
    )
    if api_key:
        st.success("API Key is actively configured.")
    else:
        st.error("API Key missing. Please update config.py.")


# ---------------------------------------------------------------------------
# Main header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🌾 AgriSense AI</div>
        <div class="hero-subtitle">
            Your simple AI-powered farming companion for smarter crop and field decisions.
            Get practical guidance without needing to understand the technology behind it.
        </div>
        <div class="hero-badge">Wheat • Cotton • Rice • Tomato</div>
    </div>
    """,
    unsafe_allow_html=True,
)

feature_cols = st.columns(3)
features = [
    ("💬", "Ask in simple words", "Get agricultural guidance from trusted crop knowledge."),
    ("🌦️", "Weather-aware advice", "Recommendations consider current field conditions and forecast."),
    ("🤖", "Smart field analysis", "The AI combines several sources before suggesting one action."),
]
for col, (icon, title, text) in zip(feature_cols, features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-text">{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

tab1, tab2, tab3 = st.tabs(
    ["💬 Ask AgriSense", "🤖 My Field Advisor", "📋 My Decisions"]
)


# ---------------------------------------------------------------------------
# TAB 1: Chat Assistant - Generative AI + RAG
# ---------------------------------------------------------------------------
with tab1:
    st.markdown('<div class="section-kicker">Farming help</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">What would you like to know?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper">Ask a question about irrigation, crop growth, nutrients, pests, or other farming problems. You can write naturally.</div>',
        unsafe_allow_html=True,
    )

    crop_options = ["Any crop", "wheat", "cotton", "rice", "tomato", "general_ipm"]
    selected_crop = st.selectbox(
        "Crop (optional)",
        crop_options,
        format_func=lambda x: "General farming" if x == "Any crop" else x.replace("_", " ").title(),
    )

    question = st.text_area(
        "Your question",
        placeholder="Example: My wheat is at tillering stage. When should I irrigate it?",
        height=105,
        label_visibility="visible",
    )

    # -----------------------------------------------------------------
    # Optional live-data link: lets the chat assistant pull in the same
    # weather + field data the Field Advisor agent uses, so questions
    # like "should I water today?" can be answered with real conditions
    # instead of general document text alone.
    # -----------------------------------------------------------------
    include_live_data = st.checkbox(
        "🌦️ Also consider my field's current weather & soil conditions",
        value=False,
        help="Turn this on for questions like 'should I irrigate today?' — "
             "the assistant will check your field's live weather and soil data "
             "before answering, the same way the Field Advisor does.",
    )

    selected_field_id_for_chat = None
    if include_live_data:
        field_ids = weather.get_available_fields()
        
        if field_ids:
            chat_field_labels = {}
            # Loop through IDs to fetch details and build the dropdown labels
            for f_id in field_ids:
                f_details = weather.get_field_status(f_id)
                if "error" not in f_details:
                    label = f"{f_details['field_id']} — {f_details['field_name']} ({f_details['crop'].title()})"
                    chat_field_labels[label] = f_details["field_id"]
                    
            chat_field_choice = st.selectbox(
                "Which field is this about?",
                list(chat_field_labels.keys()),
                key="chat_field_selector",
            )
            selected_field_id_for_chat = chat_field_labels[chat_field_choice]
        else:
            st.warning("No field information is available, so live data can't be included right now.")

    ask_col, hint_col = st.columns([1, 2])
    with ask_col:
        ask_clicked = st.button("🌱 Get Farming Advice", type="primary", use_container_width=True)
    with hint_col:
        st.caption("Tip: Include the crop and growth stage when you know them.")

    if ask_clicked:
        if not question.strip():
            st.warning("Please write your farming question first.")
        elif not api_key:
            st.error("AI advice is unavailable because the Gemini API key is not configured.")
        else:
            crop_filter = None if selected_crop == "Any crop" else selected_crop
            try:
                with st.status("🌱 Preparing your answer...", expanded=False) as status:
                    st.write("Finding the most relevant agricultural information...")
                    chunks = rag.retrieve_context(question)

                    # If the farmer asked for live data to be included, fetch
                    # the same field + weather information the Field Advisor
                    # agent uses, and fold it in as extra context alongside
                    # the retrieved documents.
                    live_field_data = None
                live_chunks = []

                if include_live_data and selected_field_id_for_chat:
                    st.write("Checking your field's current condition...")
                    live_field_data = weather.get_field_status(selected_field_id_for_chat)

                    if "error" not in live_field_data:
                        live_chunks.append({
                            "source": "Live Field Telemetry",
                            "crop": live_field_data.get("crop", "unknown"),
                            "text": f"Current conditions for {live_field_data.get('field_name')}: Soil Moisture is {live_field_data.get('soil_moisture_pct')}%, Growth Stage is {live_field_data.get('growth_stage')}, Days since last irrigated: {live_field_data.get('last_irrigated_days_ago')}."
                        })

                if not chunks and not live_field_data:
                    status.update(label="No matching guidance found", state="error")
                    st.warning("I could not find enough relevant information. Try using the crop name or rephrasing your question.")
                else:
                    st.write("Creating a clear answer from the retrieved information...")
                    # Pass chunks (strings) and live_field_data (dict) separately to LLM
                    answer = llm.generate_answer(question, chunks, live_field_data)
                    status.update(label="Answer ready", state="complete")
            
                    st.markdown('<div class="section-kicker">Your answer</div>', unsafe_allow_html=True)
                    st.markdown("### 🌱 Practical guidance")
                    safe_answer = html.escape(answer).replace("\n", "<br>")
                    st.markdown(
                        f'<div class="ai-answer" style="color:#183b29 !important; background:#ffffff !important;">{safe_answer}</div>',
                        unsafe_allow_html=True,
                    )
                    with st.expander("📚 Information used for this answer"):
                        if live_chunks:
                            st.markdown("**📡 Live data considered:**")
                            for chunk in live_chunks:
                                st.markdown(f"- **{chunk['source']}**")
                                st.caption(chunk["text"][:350] + ("..." if len(chunk["text"]) > 350 else ""))
                        st.markdown("**📚 Document sources:**")
                        for i, chunk in enumerate(chunks, 1):
                            st.markdown(f"**{i}. Agronomy Knowledge Base**")
                            st.caption(chunk[:350] + ("..." if len(chunk) > 350 else ""))    

            except Exception as e:
                st.error(f"We couldn't generate the answer right now. Please try again.\n\nTechnical detail: {e}")


# ---------------------------------------------------------------------------
# TAB 2: Farm Agent - Agentic AI
# ---------------------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-kicker">Smart field check</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Get a recommendation for your field</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper">Select your field and AgriSense will check the field data, weather forecast, and agricultural knowledge before suggesting one practical next step.</div>',
        unsafe_allow_html=True,
    )

    all_fields_ids = weather.get_available_fields()
    if not all_fields_ids:
        st.error("No field information is available.")
    else:
        field_labels = {}
        for f_id in all_fields_ids:
            f_details = weather.get_field_status(f_id)
            if "error" not in f_details:
                label = f"{f_details['field_id']} — {f_details['field_name']} ({f_details['crop'].title()})"
                field_labels[label] = f_id

        selected_label = st.selectbox("Choose your field", list(field_labels.keys()))
        selected_field_id = field_labels[selected_label]

        previous_field = st.session_state.get("last_field_id")
        if previous_field != selected_field_id:
            st.session_state["last_field_id"] = selected_field_id
            st.session_state.pop("last_result", None)

        field_preview = weather.get_field_status(selected_field_id)

        st.markdown("#### 🌱 Your field today")
        metric_cols = st.columns(4)
        metric_cols[0].metric("Crop", field_preview["crop"].title())
        metric_cols[1].metric("Soil moisture", f"{field_preview['soil_moisture_pct']}%")
        metric_cols[2].metric("Growth stage", field_preview["growth_stage"])
        metric_cols[3].metric("Last irrigation", f"{field_preview['last_irrigated_days_ago']} days ago")

        with st.expander("📊 More field information", expanded=False):
            info_cols = st.columns(3)
            info_cols[0].metric("Nitrogen (N)", field_preview["N"])
            info_cols[1].metric("Phosphorus (P)", field_preview["P"])
            info_cols[2].metric("Potassium (K)", field_preview["K"])
            st.caption(f"Soil pH: {field_preview['ph']} · Field: {field_preview['field_name']}")

        st.markdown("")
        run_clicked = st.button(
            "🤖 Analyze My Field",
            type="primary",
            use_container_width=True,
        )

        if run_clicked:
            if not api_key:
                st.error("AI recommendations are unavailable because the Gemini API key is not configured.")
            else:
                start_time = time.time()
                try:
                    with st.status("🤖 Checking your field...", expanded=True) as status:
                        st.write("✓ Reading your field conditions")
                        live_status = weather.get_field_status(selected_field_id)
                        
                        st.write("✓ Finding relevant crop guidance")
                        auto_query = f"Provide a practical farming recommendation based on current soil moisture ({live_status.get('soil_moisture_pct')}%) and growth stage ({live_status.get('growth_stage')})."
                        docs = rag.retrieve_context(auto_query)
                        
                        st.write("⏳ Combining the information into one recommendation...")
                        recommendation = llm.generate_answer(auto_query, docs, live_status)

                        # Package the result exactly how the UI expects it below
                        result = {
                            "urgency": "Medium", 
                            "recommendation": recommendation,
                            "reasoning": "Based on live field telemetry and retrieved agronomy documents.",
                            "field": live_status,
                            "rag_chunks": docs,
                            "weather_summary": f"Current Soil Moisture: {live_status.get('soil_moisture_pct')}%, Last Irrigated: {live_status.get('last_irrigated_days_ago')} days ago.",
                            "field_summary": f"Plot: {live_status.get('field_name')} | Crop: {live_status.get('crop').title()} ({live_status.get('growth_stage')})"
                        }
                    
                        elapsed = time.time() - start_time

                        status.update(
                            label=f"Recommendation ready ({elapsed:.1f}s)",
                            state="complete",
                            expanded=False,
                        )

                    st.session_state["last_result"] = result
                except Exception as e:
                    st.error(
                        "The field analysis could not be completed. Please check your internet connection and try again."
                    )
                    with st.expander("Technical error details"):
                        st.code(str(e))

        if "last_result" in st.session_state:
            result = st.session_state["last_result"]

            st.markdown("---")
            st.markdown('<div class="section-kicker">AI field advice</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Your recommended next step</div>', unsafe_allow_html=True)

            urgency = str(result.get("urgency", "Medium")).strip().title()
            urgency_class = {
                "High": "pill-high",
                "Medium": "pill-medium",
                "Low": "pill-low",
            }.get(urgency, "pill-neutral")
            urgency_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(urgency, "⚪")

            st.markdown(
                f'<span class="pill {urgency_class}">{urgency_icon} {urgency} priority</span>',
                unsafe_allow_html=True,
            )

            recommendation = html.escape(str(result.get("recommendation", "No recommendation was returned.")))
            st.markdown(
                f"""
                <div class="recommendation-card">
                    <div class="recommendation-label">Recommended action</div>
                    <div class="recommendation-text">{recommendation}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("#### Why this was recommended")
            st.write(result.get("reasoning", "The AI did not return additional reasoning."))

            with st.expander("🔎 See supporting information", expanded=False):
                st.markdown("**Field conditions**")
                st.text(result.get("field_summary", "Not available."))

                st.markdown("**Weather checked**")
                st.text(result.get("weather_summary", "Not available."))

                st.markdown("**Agricultural knowledge retrieved**")
                for i, chunk in enumerate(result.get("rag_chunks", []), 1):
                    chunk_text = str(chunk)
                    st.caption(f"[{i}] Agronomy Database — {chunk_text[:250]}{'...' if len(chunk_text) > 250 else ''}")

            st.markdown("#### 👨‍🌾 Your decision")
            st.caption("The recommendation will not be applied automatically. You decide what to do.")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Approve advice", type="primary", use_container_width=True):
                    log_decision(
                        result["field"]["field_id"],
                        result["field"]["field_name"],
                        result["recommendation"],
                        "Approved",
                    )
                    st.session_state["last_decision"] = "Approved"
                    st.success("Your approval has been recorded.")

            with col_b:
                if st.button("❌ Reject advice", use_container_width=True):
                    log_decision(
                        result["field"]["field_id"],
                        result["field"]["field_name"],
                        result["recommendation"],
                        "Rejected",
                    )
                    st.session_state["last_decision"] = "Rejected"
                    st.warning("Your rejection has been recorded.")


# ---------------------------------------------------------------------------
# TAB 3: Decision Log
# ---------------------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-kicker">Your history</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">My Decisions</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper">A simple record of recommendations you approved or rejected.</div>',
        unsafe_allow_html=True,
    )

    log_rows = load_decision_log()
    if not log_rows:
        st.info("No decisions have been recorded yet. Run the Field Advisor first.")
    else:
        approved = sum(1 for row in log_rows if row.get("human_decision") == "Approved")
        rejected = sum(1 for row in log_rows if row.get("human_decision") == "Rejected")

        stat_cols = st.columns(3)
        stat_cols[0].metric("Total decisions", len(log_rows))
        stat_cols[1].metric("Approved", approved)
        stat_cols[2].metric("Rejected", rejected)

        display_rows = [
            {
                "Date & time": row.get("timestamp", ""),
                "Field": row.get("field_name", row.get("field_id", "")),
                "Recommendation": row.get("recommendation", ""),
                "Decision": row.get("human_decision", ""),
            }
            for row in reversed(log_rows)
        ]
        st.dataframe(display_rows, use_container_width=True, hide_index=True)