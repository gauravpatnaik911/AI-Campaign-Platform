"""
Tiger Analytics | Sense & Respond OS
Multimodal Agentic Operating System — Bleeding Signals Engine
Powered by Groq (llama-3.3-70b-versatile) + SMART Signal Framework
"""

import streamlit as st
import json
import os
import time
import re
import csv
import io
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tiger Analytics | Sense & Respond OS",
    page_icon="🐯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────
# LOGO — pinned top-left
# ─────────────────────────────────────────────────────
if Path("tiger_logo.png").exists():
    st.logo("tiger_logo.png")

# ─────────────────────────────────────────────────────
# CUSTOM CSS — Tiger Analytics brand
# ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --tiger-orange: #F5A623;
    --tiger-dark:   #0D0D0D;
    --tiger-mid:    #1A1A1A;
    --tiger-card:   #111111;
    --tiger-border: #2A2A2A;
    --tiger-text:   #E8E8E8;
    --tiger-muted:  #888888;
    --tiger-red:    #FF3B30;
    --tiger-green:  #30D158;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: var(--tiger-dark) !important;
    color: var(--tiger-text) !important;
}

/* Top header bar → Tiger Orange */
header[data-testid="stHeader"] {
    background-color: var(--tiger-orange) !important;
    border-bottom: 2px solid #c8860f !important;
}
header[data-testid="stHeader"] * { color: var(--tiger-dark) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--tiger-mid) !important;
    border-right: 1px solid var(--tiger-border) !important;
}
[data-testid="stSidebar"] * { color: var(--tiger-text) !important; }

/* Buttons → black bg, orange border, orange-fill on hover */
div.stButton > button {
    background-color: #111111 !important;
    color: var(--tiger-orange) !important;
    border: 1px solid var(--tiger-orange) !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.18s ease !important;
}
div.stButton > button:hover {
    background-color: var(--tiger-orange) !important;
    color: #000 !important;
    box-shadow: 0 0 12px rgba(245,166,35,0.45) !important;
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: #1C1C1C !important;
    border-color: var(--tiger-border) !important;
    color: var(--tiger-text) !important;
}
textarea {
    background-color: #1C1C1C !important;
    color: var(--tiger-text) !important;
    border: 1px solid var(--tiger-border) !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* Tabs */
div[data-testid="stTabs"] button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    color: var(--tiger-muted) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--tiger-orange) !important;
    border-bottom: 2px solid var(--tiger-orange) !important;
}

/* Metrics */
div[data-testid="stMetric"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.14em !important;
    color: var(--tiger-muted) !important;
    text-transform: uppercase !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--tiger-orange) !important;
}

/* Expander */
details summary {
    color: var(--tiger-orange) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--tiger-mid); }
::-webkit-scrollbar-thumb { background: var(--tiger-border); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--tiger-orange); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# CONFIG REGISTRY  (mirrors n8n 00_Config_Registry)
# ─────────────────────────────────────────────────────
CONFIG = {
    "taxonomy": {
        "cpg":    {"label": "Consumer Packaged Goods",  "sub_industries": ["Beauty & Personal Care", "Food & Beverage", "Home Care", "Health & Wellness"]},
        "retail": {"label": "Retail & E-Commerce",      "sub_industries": ["Fashion & Apparel", "Luxury Goods", "Sports & Outdoor", "Home Furnishings"]},
        "media":  {"label": "Media & Entertainment",    "sub_industries": ["Streaming & OTT", "Gaming", "Social Platforms", "Live Events"]},
        "tech":   {"label": "Technology",               "sub_industries": ["AI/ML Tooling", "SaaS B2B", "Consumer Apps", "Developer Infra"]},
        "fsi":    {"label": "Financial Services",       "sub_industries": ["Retail Banking", "Wealth Management", "InsurTech", "Crypto & DeFi"]},
    },
    "functional_domains": [
        "Brand Management", "Demand Planning", "Channel Analytics",
        "Supply Chain", "Product Innovation", "Customer Experience",
        "Risk & Compliance", "Data Engineering", "Marketing Science",
    ],
    "persona_routes": {
        "Brand Manager":      {"layer": "Strategic",   "branch": "commercial_with_review",  "icon": "🎯"},
        "Demand Planner":     {"layer": "Operational", "branch": "execution_with_review",   "icon": "📦"},
        "Data Scientist":     {"layer": "Analytical",  "branch": "evidence_artifact",       "icon": "🔬"},
        "Data Engineer":      {"layer": "Technical",   "branch": "technical_artifact",      "icon": "⚙️"},
        "Compliance Officer": {"layer": "Governance",  "branch": "risk_review_only",        "icon": "🛡️"},
    },
    "model": "llama-3.3-70b-versatile",
}

BRANCH_LABELS = {
    "commercial_with_review": "Campaign Strategy + Risk Review",
    "execution_with_review":  "Execution Checklist + Risk Review",
    "evidence_artifact":      "Evidence Matrix + Scoring Logic",
    "technical_artifact":     "Data Flow + Integration Spec",
    "risk_review_only":       "Compliance + Governance Review",
}

REVIEW_BRANCHES = {"commercial_with_review", "execution_with_review",
                   "field_action_with_review", "risk_review_only"}

# ─────────────────────────────────────────────────────
# GROQ CLIENT
# ─────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client(api_key: str = ""):
    try:
        from groq import Groq
        key = api_key or os.environ.get("GROQ_API_KEY", "")
        if not key:
            return None
        return Groq(api_key=key)
    except ImportError:
        return None

# ─────────────────────────────────────────────────────
# SYSTEM PROMPTS — SMART Bleeding Signal Framework
# ─────────────────────────────────────────────────────
SYNTHESIS_SYS = """You are TigerTrend's Synthesis Agent — an elite cultural intelligence analyst.
Your ONLY job is to detect BLEEDING SIGNALS: early, high-velocity, LOW-SATURATION micro-trends.

STRICT PROHIBITIONS — NEVER output:
- Generic keywords: "casual wear", "healthy food", "digital marketing", "sustainability", "innovation"
- Broad category labels or obvious mainstream trends
- Fabricated velocity numbers with no basis in the uploaded context

SMART BLEEDING SIGNAL FRAMEWORK (mandatory for every signal):
- Specific: hyper-niche subculture or micro-aesthetic (e.g. "gorpcore utility vest", "dark academia corsetry", "whimsy-goth maximalism")
- Measurable: assign bleeding_edge_virality_score (1–100) and velocity_metric (e.g. "+400% in 48hrs")
- Actionable: keyword must be directly usable as an Imagen 3 generation prompt
- Relevant & Time-bound: must be grounded in the uploaded context and an emergence_window

EXTREME VIRALITY RULE: If bleeding_edge_virality_score >= 85, MUST set is_extreme_virality=true
and write a mandatory extreme_action_directive (e.g. "MANDATORY FAST-TRACK: Deploy counter-campaign within 48h").

Return ONLY a valid JSON object — no markdown fences, no explanation, no preamble:
{
  "smart_signals": [
    {
      "niche_keyword": "...",
      "bleeding_edge_virality_score": 0,
      "velocity_metric": "...",
      "emergence_window": "...",
      "actionability_rating": "...",
      "is_extreme_virality": false,
      "extreme_action_directive": ""
    }
  ],
  "persona_specific_data": {}
}"""

ORCH_SYS_TMPL = "You are TigerTrend's Orchestration Agent for the {layer} layer. Be hyper-specific. Reference exact signal keywords. No generic advice."

REFLECT_SYS = "You are TigerTrend's Reflection Agent — Tiger Analytics' internal governance reviewer. Be rigorous."

# ─────────────────────────────────────────────────────
# PROMPT BUILDERS
# ─────────────────────────────────────────────────────
def build_synthesis_prompt(ctx: dict, uploaded_text: str) -> str:
    industry_label = CONFIG["taxonomy"].get(ctx["industry_id"], {}).get("label", ctx["industry_id"])
    p = f"""CONTEXT:
Industry: {industry_label}  |  Sub-Industry: {ctx['sub_industry']}
Functional Domain: {ctx['functional_domain']}
Persona: {ctx['persona_role']} ({ctx['persona_layer']})
Region: {ctx.get('region','North America')}  |  Time Window: {ctx.get('time_window','Last 7 days')}
Brand Context: {ctx.get('brand_context','Not specified')}
"""
    if uploaded_text.strip():
        p += f"\nUPLOADED SIGNAL DATA (mine for bleeding signals):\n{uploaded_text[:3000]}\n"

    p += f"""
TASK: Extract 4-6 BLEEDING SIGNALS from the above context.
Persona routing hint:
- Brand Manager → campaign-ready cultural micro-aesthetics
- Data Scientist → quantifiable acceleration signals with evidence rationale
- Demand Planner → supply-chain-visible emerging product demand signals
- Data Engineer → data-source reliability / velocity computation signals
- Compliance Officer → brand-safety risks and regulatory edge signals

Return ONLY the JSON object. No markdown. No extra text."""
    return p


def build_orchestration_prompt(persona: str, branch: str, signals: list, brand_ctx: str) -> str:
    artifact_map = {
        "commercial_with_review":  "a campaign brief with 3 distinct ad angles, channel recommendations, and next-best-action table",
        "execution_with_review":   "a prioritised 48-hour execution checklist with inventory, pricing, and operational actions",
        "evidence_artifact":       "an evidence matrix with scoring assumptions, confidence intervals, and measurement plan",
        "technical_artifact":      "a data-flow specification with API integration points, reliability risks, and pipeline design",
        "risk_review_only":        "a compliance risk register with brand-safety flags, regulatory exposure, and human-review triggers",
        "field_action_with_review":"a field playbook with customer talking points, objection handlers, and upsell opportunities",
    }
    artifact = artifact_map.get(branch, "a strategic intelligence brief")
    sigs = "\n".join([
        f"  [{s.get('bleeding_edge_virality_score','?')}/100 | Arb:{s.get('arbitrage_index','?')}] "
        f"{s.get('niche_keyword','?')} — {s.get('velocity_metric','?')} | {s.get('emergence_window','?')}"
        for s in signals
    ])
    return f"""Persona: {persona} (branch: {branch})
Brand Context: {brand_ctx or 'Not specified'}

TOP BLEEDING SIGNALS:
{sigs}

Deliver {artifact}.
Every single recommendation MUST trace back to a named signal above.
Use markdown with clear headers. Be precise and actionable."""


def build_reflection_prompt(proposed: str, persona: str) -> str:
    return f"""Persona requesting review: {persona}

PROPOSED OUTPUT TO REVIEW:
{proposed[:3000]}

Review systematically for:
1. Unsupported velocity claims or hallucinated facts
2. Brand safety issues and reputational risks
3. Regulatory / compliance exposure
4. Overconfident language without evidence anchors
5. Items requiring mandatory human review

Return a structured markdown report with these sections:
## ✅ Cleared Items
## ⚠️ Risks Flagged  
## 🛑 Human Review Required"""

# ─────────────────────────────────────────────────────
# SCORING LAYER  (mirrors n8n Score Acceleration node)
# ─────────────────────────────────────────────────────
def score_signals(signals: list) -> list:
    scored = []
    for s in signals:
        virality   = s.get("bleeding_edge_virality_score", 50)
        keyword    = s.get("niche_keyword", "")
        velocity   = s.get("velocity_metric", "")

        specificity_bonus = min(len(keyword.split()) * 3 + keyword.count("-") * 4, 20)
        social_bonus = 8 if any(w in velocity.lower()
                                for w in ["tiktok","reddit","social","mention","post","share"]) else 0
        blog_bonus   = 5 if any(w in velocity.lower()
                                for w in ["blog","editorial","publication","press"]) else 0

        acceleration_score = min(int(virality * 0.6 + specificity_bonus + social_bonus + blog_bonus), 100)

        if virality >= 85:
            saturation_risk = "HIGH"
        elif virality >= 60:
            saturation_risk = "MEDIUM"
        else:
            saturation_risk = "LOW"

        saturation_bonus = {"LOW": 20, "MEDIUM": 10, "HIGH": 0}[saturation_risk]
        arbitrage_index  = round(virality * 0.4 + acceleration_score * 0.4 + saturation_bonus * 0.2, 1)

        scored.append({**s,
                       "acceleration_score": acceleration_score,
                       "saturation_risk":    saturation_risk,
                       "arbitrage_index":    arbitrage_index})

    scored.sort(key=lambda x: x.get("arbitrage_index", 0), reverse=True)
    return scored

# ─────────────────────────────────────────────────────
# AGENT RUNNER  (mirrors n8n 01_Agent_Runner)
# ─────────────────────────────────────────────────────
def run_agent(client, system: str, user_msg: str, max_tokens: int = 900, expect_json: bool = True):
    if client is None:
        err = {"error": "Groq client not initialised — check GROQ_API_KEY"}
        return err if expect_json else "⚠️ Groq client not initialised."
    try:
        resp = client.chat.completions.create(
            model=CONFIG["model"],
            messages=[{"role": "system", "content": system},
                      {"role": "user",   "content": user_msg}],
            temperature=0.2,
            max_tokens=max_tokens,
        )
        content = resp.choices[0].message.content.strip()
        if not expect_json:
            return content
        clean = re.sub(r"```(?:json)?|```", "", content).strip()
        return json.loads(clean)
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse error: {e}", "raw_output": content}
    except Exception as e:
        return {"error": str(e)} if expect_json else f"⚠️ Agent error: {e}"

# ─────────────────────────────────────────────────────
# FILE PARSER
# ─────────────────────────────────────────────────────
def parse_file(f) -> tuple[str, str]:
    name = f.name.lower()
    if name.endswith((".png", ".jpg", ".jpeg")):
        return "", "image"
    if name.endswith(".csv"):
        try:
            content = f.read().decode("utf-8", errors="ignore")
            rows = [", ".join(r) for r in csv.reader(io.StringIO(content))]
            return "\n".join(rows[:120]), "csv"
        except Exception:
            return "", "csv"
    if name.endswith(".txt"):
        return f.read().decode("utf-8", errors="ignore")[:4000], "txt"
    return "", "unknown"

# ─────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────
for k, v in {
    "chat_history":          [],
    "scored_signals":        [],
    "orchestration_output":  "",
    "reflection_output":     "",
    "pipeline_ran":          False,
    "last_ctx":              {},
    "groq_key":              "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────
# ══════════════════  SIDEBAR  ════════════════════════
# ─────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
    <div style="padding:0.6rem 0 1rem;border-bottom:1px solid #2A2A2A;margin-bottom:1rem;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;
                  letter-spacing:0.22em;color:#F5A623;text-transform:uppercase;">
        SENSE &amp; RESPOND OS</div>
      <div style="font-size:1.05rem;font-weight:700;color:#E8E8E8;margin-top:0.2rem;">
        Bleeding Signals Engine</div>
    </div>""", unsafe_allow_html=True)

    # API Key
    env_key = os.environ.get("GROQ_API_KEY", "")
    if env_key:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.68rem;'
                    'color:#30D158;margin-bottom:0.5rem;">● GROQ CONNECTED</div>',
                    unsafe_allow_html=True)
        groq_client = get_groq_client(env_key)
    else:
        api_input = st.text_input("🔑 Groq API Key", type="password",
                                  placeholder="gsk_...", key="api_key_input")
        if api_input:
            st.session_state.groq_key = api_input
        groq_client = get_groq_client(st.session_state.groq_key)
        if groq_client:
            st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.68rem;'
                        'color:#30D158;">● CONNECTED</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── CONTEXT
    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.65rem;'
                'letter-spacing:0.18em;color:#F5A623;margin-bottom:0.5rem;">▸ CONTEXT</div>',
                unsafe_allow_html=True)

    industry_id = st.selectbox("Industry",
                                options=list(CONFIG["taxonomy"].keys()),
                                format_func=lambda k: CONFIG["taxonomy"][k]["label"])
    sub_industry = st.selectbox("Sub-Industry",
                                 CONFIG["taxonomy"][industry_id]["sub_industries"])
    functional_domain = st.selectbox("Functional Domain", CONFIG["functional_domains"])
    region = st.selectbox("Region", ["North America", "EMEA", "APAC", "LATAM", "Global"])
    time_window = st.selectbox("Signal Window",
                                ["Last 24 hours", "Last 48 hours", "Last 7 days", "Last 30 days"])
    brand_context = st.text_area("Brand Context (optional)",
                                  placeholder="e.g. Premium beauty brand targeting Gen Z…",
                                  height=64)

    st.markdown("---")

    # ── PERSONA
    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.65rem;'
                'letter-spacing:0.18em;color:#F5A623;margin-bottom:0.5rem;">▸ PERSONA ENGINE</div>',
                unsafe_allow_html=True)

    selected_persona = st.radio(
        "Operational Persona",
        options=list(CONFIG["persona_routes"].keys()),
        format_func=lambda p: f"{CONFIG['persona_routes'][p]['icon']}  {p}",
    )
    pdata  = CONFIG["persona_routes"][selected_persona]
    branch = pdata["branch"]

    st.markdown(f"""
    <div style="background:#111;border:1px solid #2A2A2A;border-left:3px solid #F5A623;
                border-radius:4px;padding:0.5rem 0.7rem;margin:0.4rem 0 0.6rem;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;color:#555;
                  text-transform:uppercase;letter-spacing:0.12em;">Layer → Branch</div>
      <div style="font-size:0.78rem;color:#E8E8E8;margin-top:0.15rem;">
        {pdata['layer']} → {BRANCH_LABELS.get(branch, branch)}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── FILE UPLOAD
    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.65rem;'
                'letter-spacing:0.18em;color:#F5A623;margin-bottom:0.5rem;">▸ SIGNAL UPLOAD</div>',
                unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop signal data",
        type=["png", "jpg", "jpeg", "csv", "txt"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
        icon_map = {"png": "🖼️", "jpg": "🖼️", "jpeg": "🖼️", "csv": "📊", "txt": "📄"}
        st.markdown(f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.7rem;'
                    f'color:#30D158;">{icon_map.get(ext,"📎")} {uploaded_file.name}</div>',
                    unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.7rem;'></div>", unsafe_allow_html=True)
    run_pipeline = st.button("⚡  DETECT BLEEDING SIGNALS", use_container_width=True)

    st.markdown("---")

    # ── CHAT
    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.65rem;'
                'letter-spacing:0.18em;color:#F5A623;margin-bottom:0.5rem;">▸ COMMAND INTERFACE</div>',
                unsafe_allow_html=True)

    chat_box = st.container(height=260)
    with chat_box:
        if not st.session_state.chat_history:
            st.markdown('<div style="font-size:0.75rem;color:#444;font-style:italic;">'
                        'Awaiting first signal…</div>', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            clr   = "#F5A623" if msg["role"] == "assistant" else "#E8E8E8"
            label = "OS" if msg["role"] == "assistant" else "YOU"
            st.markdown(f"""
            <div style="margin-bottom:0.55rem;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;
                           color:{clr};letter-spacing:0.1em;">{label}</span>
              <div style="font-size:0.76rem;color:#CCC;margin-top:0.1rem;
                          line-height:1.45;">{msg['content']}</div>
            </div>""", unsafe_allow_html=True)

    chat_input = st.chat_input("Ask the OS…")

    if st.button("🗑  Clear Session", use_container_width=True):
        for k in ["chat_history", "scored_signals", "orchestration_output",
                  "reflection_output", "last_ctx"]:
            st.session_state[k] = [] if isinstance(st.session_state[k], list) else ""
        st.session_state.pipeline_ran = False
        st.rerun()


# ─────────────────────────────────────────────────────
# ═══════════════  PIPELINE EXECUTION  ════════════════
# ─────────────────────────────────────────────────────
if run_pipeline:
    persona_route = CONFIG["persona_routes"][selected_persona]
    ctx = {
        "industry_id":       industry_id,
        "sub_industry":      sub_industry,
        "functional_domain": functional_domain,
        "persona_role":      selected_persona,
        "persona_layer":     persona_route["layer"],
        "branch":            persona_route["branch"],
        "region":            region,
        "time_window":       time_window,
        "brand_context":     brand_context,
    }
    st.session_state.last_ctx = ctx

    uploaded_text, file_type = "", "none"
    if uploaded_file:
        uploaded_file.seek(0)
        uploaded_text, file_type = parse_file(uploaded_file)

    # ── Stage 1: Synthesis Agent
    with st.spinner("🔍  Synthesis Agent scanning for bleeding signals…"):
        synth_result = run_agent(
            groq_client,
            SYNTHESIS_SYS,
            build_synthesis_prompt(ctx, uploaded_text),
            max_tokens=1400,
            expect_json=True,
        )

    if isinstance(synth_result, dict) and "error" in synth_result:
        st.error(f"Synthesis Agent error: {synth_result['error']}")
        if "raw_output" in synth_result:
            with st.expander("Raw LLM output"):
                st.code(synth_result["raw_output"])
    else:
        raw_signals = synth_result.get("smart_signals", [])

        # ── Stage 2: Score
        scored = score_signals(raw_signals)
        st.session_state.scored_signals = scored

        # ── Stage 3: Orchestration Agent
        branch = ctx["branch"]
        with st.spinner(f"🤖  Orchestration Agent building {BRANCH_LABELS.get(branch, branch)}…"):
            orch = run_agent(
                groq_client,
                ORCH_SYS_TMPL.format(layer=persona_route["layer"]),
                build_orchestration_prompt(selected_persona, branch, scored[:4], brand_context),
                max_tokens=1600,
                expect_json=False,
            )
        st.session_state.orchestration_output = orch if isinstance(orch, str) else str(orch)

        # ── Stage 4: Reflection Agent (review branches only)
        if branch in REVIEW_BRANCHES:
            with st.spinner("🛡️  Reflection Agent running governance review…"):
                ref = run_agent(
                    groq_client,
                    REFLECT_SYS,
                    build_reflection_prompt(st.session_state.orchestration_output, selected_persona),
                    max_tokens=900,
                    expect_json=False,
                )
            st.session_state.reflection_output = ref if isinstance(ref, str) else str(ref)
        else:
            st.session_state.reflection_output = ""

        st.session_state.pipeline_ran = True

        top = scored[0] if scored else {}
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": (f"Pipeline complete. {len(scored)} bleeding signals detected. "
                        f"Top: **{top.get('niche_keyword','N/A')}** "
                        f"(Arbitrage {top.get('arbitrage_index','?')}). "
                        f"Branch: {BRANCH_LABELS.get(branch, branch)}.")
        })
        st.rerun()


# ─────────────────────────────────────────────────────
# CHAT POST-PIPELINE
# ─────────────────────────────────────────────────────
if chat_input:
    st.session_state.chat_history.append({"role": "user", "content": chat_input})

    if groq_client and st.session_state.pipeline_ran:
        sigs_ctx = "\n".join([
            f"- {s.get('niche_keyword')} | Virality:{s.get('bleeding_edge_virality_score')} "
            f"| Arb:{s.get('arbitrage_index')} | {s.get('velocity_metric')}"
            for s in st.session_state.scored_signals[:5]
        ])
        chat_sys = (f"You are TigerTrend OS — Tiger Analytics' agentic intelligence assistant.\n"
                    f"Persona: {selected_persona} | Industry: {sub_industry} | Branch: {branch}\n\n"
                    f"Active signals:\n{sigs_ctx}\n\n"
                    f"Answer concisely. Reference signals by exact name. No generic advice.")
        resp = run_agent(groq_client, chat_sys, chat_input, max_tokens=600, expect_json=False)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": resp if isinstance(resp, str) else str(resp)
        })
    elif not groq_client:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "⚠️ Groq API key required — enter it in the sidebar."
        })
    else:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Run the pipeline first to load bleeding signals."
        })
    st.rerun()


# ─────────────────────────────────────────────────────
# ════════════════  MAIN PANE  ════════════════════════
# The Generative Creative Studio
# ─────────────────────────────────────────────────────
persona_icon = CONFIG["persona_routes"][selected_persona]["icon"]
industry_label = CONFIG["taxonomy"][industry_id]["label"]

# ── OS Header
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            border-bottom:1px solid #2A2A2A;padding-bottom:0.9rem;margin-bottom:1.4rem;">
  <div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;
                letter-spacing:0.22em;color:#F5A623;text-transform:uppercase;">
      TIGER ANALYTICS / SENSE &amp; RESPOND OS</div>
    <div style="font-size:1.5rem;font-weight:700;color:#E8E8E8;margin-top:0.1rem;">
      {persona_icon} {selected_persona} Studio</div>
  </div>
  <div style="text-align:right;">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.6rem;color:#444;
                letter-spacing:0.1em;">{industry_label.upper()} / {sub_industry.upper()}</div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.68rem;
                color:#666;margin-top:0.15rem;">{datetime.now().strftime("%d %b %Y  %H:%M")}</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# IDLE STATE
# ─────────────────────────────────────────────────────
if not st.session_state.pipeline_ran:

    st.markdown("""
    <div style="border:1px solid #2A2A2A;border-radius:8px;padding:2.5rem 2rem;
                text-align:center;background:#0F0F0F;margin-top:1rem;">
      <div style="font-size:2.5rem;margin-bottom:0.7rem;">🐯</div>
      <div style="font-size:1.2rem;font-weight:600;color:#E8E8E8;margin-bottom:0.4rem;">
        Generative Creative Studio</div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:#555;
                  max-width:500px;margin:0 auto;line-height:1.8;">
        Configure context → Select persona → Upload signal data (optional)<br>
        Hit <span style="color:#F5A623;font-weight:600;">DETECT BLEEDING SIGNALS</span>
        to activate the agentic pipeline.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

    # Persona cards
    cols = st.columns(len(CONFIG["persona_routes"]))
    for col, (persona, pd) in zip(cols, CONFIG["persona_routes"].items()):
        with col:
            st.markdown(f"""
            <div style="border:1px solid #2A2A2A;border-radius:6px;padding:0.9rem 0.7rem;
                        background:#111;text-align:center;">
              <div style="font-size:1.4rem;">{pd['icon']}</div>
              <div style="font-size:0.78rem;font-weight:600;color:#E8E8E8;margin-top:0.25rem;">
                {persona}</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.55rem;
                          color:#555;margin-top:0.1rem;">{pd['layer']}</div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:0.52rem;
                          color:#333;margin-top:0.15rem;">{BRANCH_LABELS[pd['branch']]}</div>
            </div>""", unsafe_allow_html=True)

    # Pipeline diagram
    st.markdown("""
    <div style="margin-top:2rem;font-family:'IBM Plex Mono',monospace;font-size:0.6rem;
                color:#333;text-align:center;letter-spacing:0.07em;line-height:2.2;">
      CONTEXT RESOLUTION → SOURCE INGESTION → SYNTHESIS AGENT → SIGNAL SCORING<br>
      → PERSONA ROUTING → ORCHESTRATION AGENT → REFLECTION AGENT → STUDIO OUTPUT
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────
# ACTIVE STATE — pipeline has run
# ─────────────────────────────────────────────────────
else:
    scored_signals = st.session_state.scored_signals
    active_branch  = st.session_state.last_ctx.get("branch", branch)

    # ── Top-line metrics
    if scored_signals:
        top          = scored_signals[0]
        extreme_ct   = sum(1 for s in scored_signals if s.get("is_extreme_virality"))
        high_arb_ct  = sum(1 for s in scored_signals if s.get("arbitrage_index", 0) >= 70)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Signals Detected", len(scored_signals))
        m2.metric("Top Arbitrage Index", f"{top.get('arbitrage_index',0):.1f}")
        m3.metric("Extreme Virality", extreme_ct,
                  delta="⚡ Fast-Track" if extreme_ct else None)
        m4.metric("High Opportunity", high_arb_ct)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    # ── Tabs
    tab1, tab2, tab3 = st.tabs(["📡  Bleeding Signals", "📋  Persona Output", "🛡️  Governance Review"])

    # ─── TAB 1: BLEEDING SIGNAL ALERT CARDS ───────────
    with tab1:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.62rem;'
                    'letter-spacing:0.2em;color:#F5A623;margin-bottom:1rem;">'
                    '▸ CULTURAL INTELLIGENCE ALERTS — LIVE SIGNAL FEED</div>',
                    unsafe_allow_html=True)

        if not scored_signals:
            st.info("No signals detected — try adjusting context or uploading richer signal data.")
        else:
            for i, sig in enumerate(scored_signals):
                virality   = sig.get("bleeding_edge_virality_score", 0)
                arb        = sig.get("arbitrage_index", 0)
                is_ext     = sig.get("is_extreme_virality", False)
                sat        = sig.get("saturation_risk", "MEDIUM")
                acc        = sig.get("acceleration_score", 0)

                border = "#FF3B30" if is_ext else ("#F5A623" if virality >= 70 else "#2A2A2A")
                bg     = "#1A0808" if is_ext else "#0F0F0F"
                sat_c  = {"HIGH": "#FF3B30", "MEDIUM": "#F5A623", "LOW": "#30D158"}.get(sat, "#888")
                bar_c  = "#FF3B30" if is_ext else ("#F5A623" if virality >= 70 else "#30D158")

                ext_banner = ""
                if is_ext:
                    directive = sig.get("extreme_action_directive", "")
                    ext_banner = f"""
                    <div style="background:#FF3B30;color:#fff;padding:0.3rem 0.7rem;
                                border-radius:3px;font-family:'IBM Plex Mono',monospace;
                                font-size:0.62rem;letter-spacing:0.08em;margin-bottom:0.6rem;
                                font-weight:600;">⚡ EXTREME VIRALITY &nbsp;|&nbsp; {directive}</div>"""

                st.markdown(f"""
                <div style="border:1px solid {border};border-radius:6px;background:{bg};
                            padding:1rem 1.2rem;margin-bottom:0.85rem;">
                  {ext_banner}
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;
                              flex-wrap:wrap;gap:0.6rem;">
                    <div style="flex:1;min-width:200px;">
                      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.55rem;
                                  color:#444;letter-spacing:0.14em;text-transform:uppercase;">
                        SIGNAL #{i+1} &nbsp;·&nbsp; {sig.get('emergence_window','N/A')}</div>
                      <div style="font-size:1.05rem;font-weight:700;color:#F5A623;
                                  margin:0.25rem 0;font-family:'Space Grotesk',sans-serif;">
                        {sig.get('niche_keyword','N/A')}</div>
                      <div style="font-size:0.78rem;color:#AAA;">
                        {sig.get('velocity_metric','N/A')}</div>
                      <div style="font-size:0.72rem;color:#666;margin-top:0.25rem;">
                        {sig.get('actionability_rating','N/A')}</div>
                    </div>
                    <div style="display:flex;gap:0.6rem;flex-wrap:wrap;align-items:flex-start;">
                      <div style="text-align:center;background:#111;border:1px solid #2A2A2A;
                                  border-radius:4px;padding:0.45rem 0.7rem;min-width:65px;">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.52rem;
                                    color:#444;letter-spacing:0.08em;">VIRALITY</div>
                        <div style="font-size:1.25rem;font-weight:700;color:{bar_c};">{virality}</div>
                      </div>
                      <div style="text-align:center;background:#111;border:1px solid #2A2A2A;
                                  border-radius:4px;padding:0.45rem 0.7rem;min-width:65px;">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.52rem;
                                    color:#444;letter-spacing:0.08em;">ACCEL</div>
                        <div style="font-size:1.25rem;font-weight:700;color:#E8E8E8;">{acc}</div>
                      </div>
                      <div style="text-align:center;background:#111;border:1px solid #2A2A2A;
                                  border-radius:4px;padding:0.45rem 0.7rem;min-width:65px;">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.52rem;
                                    color:#444;letter-spacing:0.08em;">ARBITRAGE</div>
                        <div style="font-size:1.25rem;font-weight:700;color:#E8E8E8;">{arb:.0f}</div>
                      </div>
                      <div style="text-align:center;background:#111;border:1px solid {sat_c};
                                  border-radius:4px;padding:0.45rem 0.7rem;min-width:65px;">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.52rem;
                                    color:#444;letter-spacing:0.08em;">SAT RISK</div>
                        <div style="font-size:0.8rem;font-weight:700;color:{sat_c};">{sat}</div>
                      </div>
                    </div>
                  </div>
                  <div style="margin-top:0.8rem;background:#1A1A1A;border-radius:2px;height:3px;">
                    <div style="background:{bar_c};width:{min(virality,100)}%;height:3px;
                                border-radius:2px;"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

        # ── Imagen 3 / VTO (via subprocess to backend scripts)
        st.markdown("---")
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.62rem;'
                    'letter-spacing:0.18em;color:#F5A623;margin-bottom:0.6rem;">'
                    '▸ IMAGEN 3 GENERATIVE STUDIO</div>', unsafe_allow_html=True)

        if scored_signals:
            ic1, ic2, ic3 = st.columns([2, 1, 1])
            with ic1:
                img_signal = st.selectbox(
                    "Signal for generation",
                    [s.get("niche_keyword","") for s in scored_signals],
                )
            with ic2:
                inf_id = st.text_input("Influencer ID", value="INF001")
            with ic3:
                trend_id_val = st.text_input("Trend ID", value="TRD001")

            if st.button("🎨  Generate with Imagen 3", use_container_width=True):
                script = Path("scripts/generate_trend_image.py")
                if script.exists():
                    import subprocess
                    with st.spinner("Calling Imagen 3…"):
                        r = subprocess.run(
                            ["python", str(script),
                             "--influencer-id", inf_id,
                             "--trend-id", trend_id_val],
                            capture_output=True, text=True, timeout=120)
                    if r.returncode == 0:
                        st.success("✅ Imagen 3 generation complete")
                        st.code(r.stdout)
                        for p in list(Path("outputs").glob("*.png"))[:3] if Path("outputs").exists() else []:
                            st.image(str(p), caption=p.name, use_container_width=True)
                    else:
                        st.warning(f"Script error:\n{r.stderr}")
                else:
                    st.info("ℹ️ `scripts/generate_trend_image.py` not found. "
                            "Place it in your project root to enable Imagen 3.")

        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.62rem;'
                    'letter-spacing:0.18em;color:#F5A623;margin:1rem 0 0.6rem;">'
                    '▸ VIRTUAL TRY-ON (Google VTO)</div>', unsafe_allow_html=True)

        vc1, vc2 = st.columns(2)
        with vc1:
            vto_src = st.file_uploader("Source (person)", type=["png","jpg","jpeg"], key="vto_src")
        with vc2:
            vto_ref = st.file_uploader("Reference (garment)", type=["png","jpg","jpeg"], key="vto_ref")

        if st.button("👕  Run Virtual Try-On", use_container_width=True):
            if vto_src and vto_ref:
                script = Path("scripts/run_virtual_tryon.py")
                if script.exists():
                    import subprocess, tempfile as _tf
                    with _tf.TemporaryDirectory() as td:
                        sp = Path(td) / vto_src.name
                        rp = Path(td) / vto_ref.name
                        od = Path(td) / "out"; od.mkdir()
                        sp.write_bytes(vto_src.read())
                        rp.write_bytes(vto_ref.read())
                        with st.spinner("Running Google VTO API…"):
                            r = subprocess.run(
                                ["python", str(script),
                                 "--source", str(sp),
                                 "--reference", str(rp),
                                 "--output-dir", str(od)],
                                capture_output=True, text=True, timeout=180)
                        if r.returncode == 0:
                            imgs = list(od.glob("*.png")) + list(od.glob("*.jpg"))
                            if imgs:
                                st.success("✅ Virtual Try-On complete")
                                vcols = st.columns(len(imgs))
                                for idx, ip in enumerate(imgs):
                                    with vcols[idx]:
                                        st.image(str(ip), caption=ip.name, use_container_width=True)
                            else:
                                st.warning("VTO ran but no output images found.")
                                st.code(r.stdout)
                        else:
                            st.error(f"VTO error:\n{r.stderr}")
                else:
                    st.info("ℹ️ `scripts/run_virtual_tryon.py` not found in project root.")
            else:
                st.warning("Upload both source and reference images.")

    # ─── TAB 2: ORCHESTRATION OUTPUT ──────────────────
    with tab2:
        st.markdown(f"""
        <div style="border-left:3px solid #F5A623;padding-left:0.9rem;margin-bottom:1.2rem;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;
                      color:#666;letter-spacing:0.12em;text-transform:uppercase;">
            {pdata['layer']} LAYER OUTPUT</div>
          <div style="font-size:1.05rem;font-weight:600;color:#E8E8E8;margin-top:0.12rem;">
            {persona_icon} {selected_persona} — {BRANCH_LABELS.get(active_branch, active_branch)}</div>
        </div>""", unsafe_allow_html=True)

        if st.session_state.orchestration_output:
            st.markdown(st.session_state.orchestration_output)
            st.download_button(
                "⬇  Export as Markdown",
                data=st.session_state.orchestration_output,
                file_name=f"tigertrend_{selected_persona.lower().replace(' ','_')}"
                          f"_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.info("Orchestration Agent output will appear here after the pipeline runs.")

    # ─── TAB 3: GOVERNANCE / REFLECTION ──────────────
    with tab3:
        st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.62rem;'
                    'letter-spacing:0.2em;color:#F5A623;margin-bottom:1rem;">'
                    '▸ REFLECTION AGENT — GOVERNANCE &amp; BRAND SAFETY REVIEW</div>',
                    unsafe_allow_html=True)

        if st.session_state.reflection_output:
            st.markdown(st.session_state.reflection_output)
        elif active_branch in REVIEW_BRANCHES:
            st.info("Governance review will appear here after the pipeline runs.")
        else:
            st.markdown(f"""
            <div style="border:1px solid #2A2A2A;border-radius:6px;padding:1.2rem;
                        background:#0F0F0F;text-align:center;">
              <div style="font-size:0.82rem;color:#666;">
                Governance review is not required for the
                <strong style="color:#F5A623;">{BRANCH_LABELS.get(active_branch, active_branch)}</strong>
                branch.<br>
                <span style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:#444;">
                  Reflection Agent activates for: commercial, execution,
                  field-action, and governance routes.
                </span>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── JSON Inspector
    st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
    with st.expander("🔍  RAW PIPELINE OUTPUT — JSON Inspector"):
        payload = {
            "prototype_name":    "TigerTrend / Sense & Respond OS",
            "workflow_version":  "streamlit-groq-v1",
            "request":           st.session_state.last_ctx,
            "scored_trends":     st.session_state.scored_signals,
            "orchestration_preview": (st.session_state.orchestration_output or "")[:500],
            "reflection_preview":    (st.session_state.reflection_output or "")[:300],
            "generated_at":      datetime.now().isoformat(),
        }
        st.json(payload)
        st.download_button(
            "⬇  Export Full JSON",
            data=json.dumps({**payload,
                              "orchestration_output": st.session_state.orchestration_output,
                              "reflection_output":    st.session_state.reflection_output}, indent=2),
            file_name=f"tigertrend_pipeline_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
        )

# ─────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem;padding-top:0.8rem;border-top:1px solid #181818;
            text-align:center;font-family:'IBM Plex Mono',monospace;
            font-size:0.58rem;color:#2A2A2A;letter-spacing:0.12em;">
  TIGER ANALYTICS &nbsp;·&nbsp; SENSE &amp; RESPOND OS &nbsp;·&nbsp;
  BLEEDING SIGNALS ENGINE &nbsp;·&nbsp; GROQ + LLAMA-3.3-70B-VERSATILE
</div>""", unsafe_allow_html=True)
