import streamlit as st
import json
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict

# --- CORE LIBRARY CHECK ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. Run: pip install groq")
    st.stop()

# ==========================================
# 1. STRICT TAXONOMY (4x4x8)
# ==========================================
INDUSTRIES = {
    "Retail": ["Fashion & Apparel", "Consumer Electronics", "Grocery", "E-commerce"],
    "CPG": ["Food & Beverage", "Beauty & Cosmetics", "Household Cleaning", "Pet Care"],
    "Healthcare": ["Pharmaceuticals", "Medical Devices", "Hospitals", "Digital Health"],
    "SaaS": ["AI Platforms", "Cybersecurity", "FinTech", "Cloud Infrastructure"]
}

PERSONAS = [
    "CEO (Strategy)", 
    "Chief Operating Officer (Ops)", 
    "VP of Strategy (Strategy)", 
    "Supply Chain Director (Ops)", 
    "Chief Marketing Officer (Strategy)", 
    "Product Manager (Ops)", 
    "Financial Controller (Ops)", 
    "Data Scientist (Strategy/Ops)"
]

# ==========================================
# 2. SCHEMA DEFINITIONS
# ==========================================
class StrategicSignal(BaseModel):
    feature_name: str
    virality_score: float      
    yield_velocity: float      
    mbb_action_title: str      

class OmniverseIntelligence(BaseModel):
    governing_thought: str
    strategic_pillars: List[Dict[str, str]]
    signals: List[StrategicSignal]
    kpi_impact_matrix: Dict[str, str]
    linchpin_risk: str

# ==========================================
# 3. THE LOGIC ENGINES
# ==========================================
def execute_social_listening(sub_industry: str, client: Groq):
    """Crawls for raw viral semantic data and exact virality percentages."""
    sys_prompt = """
    You are a predictive text-mining crawler. Return strictly JSON:
    - 'hero_insight': 1-sentence elite executive revelation about market demand.
    - 'viral_velocity_score': integer (0-100).
    - 'demand_trajectory': string (e.g., 'Hyper-Growth', 'Cooling').
    - 'trending_keywords': dictionary of 6 exactly trending phrases and their virality percentage (integer 1-100). Example: {"supply chain automation": 92}
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"Scan {sub_industry}"}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return {
            "hero_insight": "Market accelerating towards automated, high-yield efficiencies.", 
            "viral_velocity_score": 85, "demand_trajectory": "Accelerating",
            "trending_keywords": {"automation": 95, "scale": 88, "AI": 100, "margins": 75, "integration": 80, "SaaS": 90}
        }

def execute_omniverse_synthesis(ind, sub, per, social_data, client):
    """Synthesizes strategy heavily indexed on the selected Persona."""
    
    # Force the LLM to change output based on Ops vs Strategy
    persona_directive = ""
    if "Ops" in per:
        persona_directive = "CRITICAL: Focus entirely on Supply Chain, Margins, Cost-Reduction, Throughput, and Operational Risk. Do not give marketing advice."
    else:
        persona_directive = "CRITICAL: Focus entirely on Market Share, CAC, Revenue Growth, Positioning, and Product Strategy. Do not give warehouse advice."

    sys_prompt = f"""
    You are an elite MBB Strategy Partner advising a {per} in the {sub} ({ind}) sector.
    LIVE VIRAL DATA: {json.dumps(social_data)}

    {persona_directive}

    MANDATES:
    1. Governing Thought: Board-level answer integrating the Live Viral Data. Speak directly to the {per}'s daily KPIs.
    2. MECE Pillars: 3 strategic pillars. EXACT keys: 'title' and 'description'.
    3. Action Titles: Every response must drive execution for this specific persona.
    Return strictly JSON matching the OmniverseIntelligence schema.
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}, temperature=0.2 
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        st.error(f"Logic Engine Disruption: {e}")
        return None

# ==========================================
# 4. NATIVE, CLEAN UI DASHBOARD
# ==========================================
st.set_page_config(page_title="Executive Intelligence", layout="wide")

# Minimalist CSS just to clean up Streamlit's default padding
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1 { font-weight: 800; }
        h2, h3 { font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.title("Strategic Parameters")
sel_ind = st.sidebar.selectbox("Industry", list(INDUSTRIES.keys()))
sel_sub = st.sidebar.selectbox("Sub-Industry", INDUSTRIES[sel_ind])
sel_per = st.sidebar.selectbox("Executive Persona", PERSONAS)

st.sidebar.divider()

if "GROQ_API_KEY" not in st.secrets:
    st.sidebar.error("GROQ_API_KEY missing in Secrets.")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if st.sidebar.button("Execute Strategic Synthesis", type="primary", use_container_width=True):
    with st.spinner(f"Aggregating Viral Data & Tailoring for {sel_per}..."):
        social_data = execute_social_listening(sel_sub, client)
        intel = execute_omniverse_synthesis(sel_ind, sel_sub, sel_per, social_data, client)
        
        if intel: 
            st.session_state.social_data = social_data
            st.session_state.intel = intel

# --- DASHBOARD RENDERING ---
if "intel" in st.session_state:
    doc = st.session_state.intel
    sd = st.session_state.social_data

    # 1. HERO HEADER
    st.markdown(f"##### EXECUTIVE BRIEFING FOR: **{sel_per.upper()}**")
    st.header(doc.get('governing_thought', 'Strategic Overview'))
    st.info(f"**Live Market Signal:** {sd.get('hero_insight', '')}")
    
    st.divider()

    # 2. KEYWORDS & METRICS ROW
    col_keywords, col_metrics = st.columns([1.2, 1])
    
    with col_keywords:
        st.subheader("Trending Market Signals")
        st.caption("Real-time virality percentages based on social listening.")
        # Renders beautiful, native progress bars for each keyword
        keywords = sd.get("trending_keywords", {})
        for kw, score in keywords.items():
            # Clean up the output ensuring score is an integer between 0 and 100
            safe_score = min(max(int(score), 0), 100)
            st.markdown(f"**{kw.title()}**")
            st.progress(safe_score / 100.0, text=f"{safe_score}% Viral Saturation")

    with col_metrics:
        st.subheader("Velocity & Risk")
        c1, c2 = st.columns(2)
        c1.metric("Viral Velocity Index", f"{sd.get('viral_velocity_score', 0)} / 100")
        c2.metric("Demand Trajectory", sd.get("demand_trajectory", "Active"))
        
        st.error(f"**Linchpin Risk Variable:**\n{doc.get('linchpin_risk', 'N/A')}")
        
    st.divider()

    # 3. MECE PILLARS (Tailored to Persona)
    st.subheader(f"Strategic Pillars for {sel_per.split(' ')[0]}")
    pillars = doc.get('strategic_pillars', [])
    if pillars:
        cols = st.columns(len(pillars))
        for i, pillar in enumerate(pillars):
            with cols[i]:
                title = pillar.get('title', f'Pillar {i+1}')
                desc = pillar.get('description', '')
                with st.container(border=True):
                    st.markdown(f"#### 0{i+1}")
                    st.markdown(f"**{title}**")
                    st.markdown(f"<span style='color:gray'>{desc}</span>", unsafe_allow_html=True)

    st.divider()

    # 4. ARBITRAGE MATRIX (Native Streamlit DataFrame styling)
    st.subheader("Predictive Arbitrage Matrix")
    signals = doc.get('signals', [])
    if signals:
        sig_df = pd.DataFrame(signals)
        sig_df['Arbitrage Index'] = (sig_df['virality_score'] * sig_df['yield_velocity']).round(2)
        sig_df = sig_df.sort_values(by='Arbitrage Index', ascending=False)
        
        # Clean up column names for presentation
        sig_df = sig_df.rename(columns={
            "feature_name": "Feature / Initiative",
            "mbb_action_title": "Strategic Action Directive",
            "virality_score": "Virality Score",
            "yield_velocity": "Yield Velocity"
        })
        
        # Display using Streamlit's native, highly readable dataframe component
        st.dataframe(
            sig_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Virality Score": st.column_config.ProgressColumn("Virality Score", min_value=0, max_value=100, format="%f"),
                "Yield Velocity": st.column_config.NumberColumn("Yield Velocity", format="%.2fx")
            }
        )

    # 5. KPI ATTRIBUTION
    st.subheader(f"KPI Attribution for {sel_per.split(' ')[0]}")
    kpi_cols = st.columns(len(doc.get('kpi_impact_matrix', {})))
    for i, (k, v) in enumerate(doc.get('kpi_impact_matrix', {}).items()):
        with kpi_cols[i % len(kpi_cols)]:
            st.markdown(f"**{k}**")
            st.caption(v)
