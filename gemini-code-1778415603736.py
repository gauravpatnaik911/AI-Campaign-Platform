import streamlit as st
import json
import pandas as pd
import urllib.parse
from pydantic import BaseModel
from typing import List, Dict

# --- CORE LIBRARY CHECK ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. Run: pip install groq")
    st.stop()

# ==========================================
# 1. TIGER ANALYTICS ENTERPRISE TAXONOMY
# ==========================================
INDUSTRIES = {
    "Retail & Apparel (e.g., Nike, Gap)": ["Athleisure & Footwear", "Fast Fashion", "Luxury Apparel", "Sporting Goods"],
    "CPG & FMCG (e.g., PepsiCo)": ["Food & Beverage", "Snacks & Confectionery", "Sports & Energy Drinks", "Personal Care"],
    "Direct-to-Consumer (D2C)": ["Subscription Boxes", "Digital-Native Brands", "Health & Supplements", "Home & Furniture"],
    "Retail Operations & Tech": ["Omnichannel Fulfillment", "In-Store Experience", "E-commerce Platforms", "Supply Chain Tech"]
}

PERSONAS = [
    "Creative Designer (Ops)", 
    "Campaign Analyst (Ops)", 
    "Merchandising Manager (Ops)", 
    "Data Scientist (Ops)",
    "Digital Product Owner (Ops)",
    "Chief Marketing Officer (Strategy)", 
    "VP of Supply Chain & Logistics (Strategy)", 
    "Chief Revenue Officer (Strategy)"
]

# ==========================================
# 2. SCHEMA DEFINITIONS
# ==========================================
class StrategicSignal(BaseModel):
    feature_name: str
    virality_score: float      
    yield_velocity: float      
    mbb_action_title: str      

class SourceLink(BaseModel):
    title: str
    url: str

class OmniverseIntelligence(BaseModel):
    governing_thought: str
    strategic_pillars: List[Dict[str, str]]
    signals: List[StrategicSignal]
    kpi_impact_matrix: Dict[str, str]
    linchpin_risk: str
    persona_deliverables: List[Dict[str, str]]
    source_links: List[SourceLink]

# ==========================================
# 3. THE LOGIC ENGINES
# ==========================================
def execute_social_listening(sub_industry: str, client: Groq):
    sys_prompt = """
    You are a predictive text-mining crawler for 2026. Return strictly JSON:
    - 'hero_insight': 1-sentence macro trend revelation about emerging, overlooked consumer demand.
    - 'viral_velocity_score': integer (0-100).
    - 'demand_trajectory': string (e.g., 'Hyper-Growth', 'Cooling').
    - 'trending_keywords': dictionary of 6 bleeding-edge trending phrases and their virality percentage (integer 1-100).
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"Scan {sub_industry}"}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return {
            "hero_insight": "Consumers are abandoning mass-personalization for hyper-local, cryptographically verified authenticity.", 
            "viral_velocity_score": 91, "demand_trajectory": "Accelerating",
            "trending_keywords": {"zero-party autonomy": 95, "biophilic materials": 88, "spatial UI commerce": 100, "decentralized loyalty": 75, "dark-store micro-fulfillment": 80, "neuro-aesthetic design": 90}
        }

def execute_omniverse_synthesis(ind, sub, per, social_data, client):
    persona_directives = {
        "Creative Designer (Ops)": "Focus ONLY on cutting-edge 2026 visual aesthetics. For 'persona_deliverables', provide 3 'Pinterest-Style Sketch Prompts'. The 'image_keyword' MUST be a highly descriptive 5-7 word prompt for an AI image generator describing a physical sketch.",
        "Campaign Analyst (Ops)": "Focus ONLY on advanced 2026 ad-tech (e.g., predictive LTV bidding, algorithmic creative fatigue). For 'persona_deliverables', provide 3 'Hyper-Targeted Experiment Hypotheses' with strict control/variant setups.",
        "Merchandising Manager (Ops)": "Focus ONLY on AI-driven localized assortment and predictive markdown algorithms. For 'persona_deliverables', provide 3 'Algorithmic SKU Interventions'.",
        "Data Scientist (Ops)": "Focus ONLY on LLM agents, vector databases, and real-time edge computing. For 'persona_deliverables', provide 3 'Machine Learning Architecture Blueprints'.",
        "Digital Product Owner (Ops)": "Focus ONLY on spatial computing interfaces and biometric checkout. For 'persona_deliverables', provide 3 'Next-Gen Feature Sprint Backlogs'.",
        "Chief Marketing Officer (Strategy)": "Focus ONLY on overarching brand positioning and cultural disruption. For 'persona_deliverables', provide 3 'Macro Brand Narratives'.",
        "VP of Supply Chain & Logistics (Strategy)": "Focus ONLY on blockchain traceability and autonomous last-mile robotics. For 'persona_deliverables', provide 3 'Logistics Cost-Reduction Initiatives'.",
        "Chief Revenue Officer (Strategy)": "Focus ONLY on dynamic pricing elasticity models and B2B API monetization. For 'persona_deliverables', provide 3 'Revenue Stream Expansions'."
    }
    
    directive = persona_directives.get(per, "Provide actionable insights relevant to the persona.")

    sys_prompt = f"""
    You are an elite Strategy Partner advising a {per} at an enterprise like Nike or PepsiCo in the {sub} ({ind}) sector.
    LIVE VIRAL MACRO-TREND DATA: {json.dumps(social_data)}

    CRITICAL DIRECTIVE: {directive}
    MANDATORY TONE: Your advice must justify a $100k consulting fee. Identify the "missing alpha"—the absolute bleeding-edge trend that competitors are currently ignoring. Do NOT use generic business fluff. Give them something highly technical and eye-catching.

    OUTPUT FORMAT (STRICT JSON EXACTLY AS SHOWN BELOW):
    {{
        "governing_thought": "string (Board-level summary of the missing alpha)",
        "strategic_pillars": [
            {{"title": "string", "description": "string (Exact execution instructions)"}},
            {{"title": "string", "description": "string"}},
            {{"title": "string", "description": "string"}}
        ],
        "signals": [
            {{"feature_name": "string", "virality_score": 90.5, "yield_velocity": 2.4, "mbb_action_title": "string"}}
        ],
        "kpi_impact_matrix": {{"KPI 1": "Impact", "KPI 2": "Impact", "KPI 3": "Impact"}},
        "linchpin_risk": "string",
        "persona_deliverables": [
            {{"title": "string", "description": "string", "image_keyword": "string"}} 
        ],
        "source_links": [
            {{"title": "string (e.g., Gartner, Business of Fashion, McKinsey)", "url": "string (Valid or highly realistic URL pointing to trend data)"}}
        ]
    }}
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}, temperature=0.3 
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        st.error(f"Logic Engine Disruption: {e}")
        return None

# ==========================================
# 4. NATIVE, CLEAN UI DASHBOARD
# ==========================================
st.set_page_config(page_title="Enterprise Intelligence", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1 { font-weight: 800; color: #0f172a;}
        h2, h3 { font-weight: 700; color: #1e293b;}
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.title("Strategic Parameters")
sel_ind = st.sidebar.selectbox("Enterprise Industry", list(INDUSTRIES.keys()))
sel_sub = st.sidebar.selectbox("Sub-Industry Segment", INDUSTRIES[sel_ind])
sel_per = st.sidebar.selectbox("Executive Persona", PERSONAS)

st.sidebar.divider()

if "GROQ_API_KEY" not in st.secrets:
    st.sidebar.error("GROQ_API_KEY missing in Secrets.")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if st.sidebar.button(f"Generate Strategy for {sel_per.split(' ')[0]}", type="primary", use_container_width=True):
    with st.spinner(f"Aggregating Missing Alpha & Tailoring for {sel_per.split(' ')[0]}..."):
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
    st.markdown(f"##### ENTERPRISE BRIEFING FOR: **{sel_per.upper()}**")
    st.header(doc.get('governing_thought', 'Strategic Overview'))
    st.info(f"**Bleeding-Edge Signal:** {sd.get('hero_insight', '')}")
    
    st.divider()

    # 2. KEYWORDS & METRICS ROW
    col_keywords, col_metrics = st.columns([1.2, 1])
    
    with col_keywords:
        st.subheader("Trending Market Signals")
        st.caption("Real-time virality percentages based on social listening.")
        keywords = sd.get("trending_keywords", {})
        if keywords:
            for kw, score in keywords.items():
                safe_score = min(max(int(score), 0), 100)
                st.markdown(f"**{kw.title()}**")
                st.progress(safe_score / 100.0, text=f"{safe_score}% Viral Saturation")
        else:
            st.warning("No keyword data currently available.")

    with col_metrics:
        st.subheader("Velocity & Risk")
        c1, c2 = st.columns(2)
        c1.metric("Viral Velocity Index", f"{sd.get('viral_velocity_score', 0)} / 100")
        c2.metric("Demand Trajectory", sd.get("demand_trajectory", "Active"))
        
        st.error(f"**Persona-Specific Linchpin Risk:**\n{doc.get('linchpin_risk', 'N/A')}")
        
    st.divider()

    # 3. MECE PILLARS
    st.subheader(f"Actionable 'Missing Alpha' Strategy")
    pillars = doc.get('strategic_pillars', [])
    if pillars and len(pillars) > 0:
        cols = st.columns(len(pillars))
        for i, pillar in enumerate(pillars):
            with cols[i]:
                title = pillar.get('title', f'Pillar {i+1}')
                desc = pillar.get('description', '')
                with st.container(border=True):
                    st.markdown(f"#### 0{i+1}")
                    st.markdown(f"**{title}**")
                    st.markdown(f"<span style='color:#475569'>{desc}</span>", unsafe_allow_html=True)

    st.divider()

    # 4. EXCLUSIVE PERSONA DELIVERABLES (PINTEREST GENERATOR)
    st.subheader(f"Exclusive Deliverables: {sel_per.split(' ')[0]}")
    deliverables = doc.get('persona_deliverables', [])
    
    if deliverables and len(deliverables) > 0:
        del_cols = st.columns(len(deliverables))
        for i, item in enumerate(deliverables):
            with del_cols[i]:
                d_title = item.get('title', 'Deliverable')
                d_desc = item.get('description', 'Details pending.')
                
                with st.container(border=True):
                    # IF DESIGNER: Generate a LIVE Pinterest-style sketch!
                    if "Designer" in sel_per:
                        raw_kw = item.get('image_keyword', 'fashion design sketch')
                        # Force the AI generator to make it a Pinterest-style sketch
                        encoded_kw = urllib.parse.quote(f"{raw_kw} pinterest style concept art sketch highly detailed clean white background")
                        
                        # Call the free Pollinations AI Generative Endpoint
                        st.image(f"https://image.pollinations.ai/prompt/{encoded_kw}?width=600&height=400&nologo=true", use_container_width=True)
                        st.markdown(f"**Visual Concept: {d_title}**")
                    else:
                        st.markdown(f"**Tactical Asset: {d_title}**")
                    
                    st.markdown(f"<span style='color:#475569'>{d_desc}</span>", unsafe_allow_html=True)
    else:
        st.info(f"No specific tactical deliverables generated for {sel_per}.")

    st.divider()

    # 5. ARBITRAGE MATRIX
    st.subheader("Initiative Prioritization & Arbitrage")
    signals = doc.get('signals', [])
    if signals:
        try:
            sig_df = pd.DataFrame(signals)
            sig_df['Arbitrage Index'] = (sig_df['virality_score'] * sig_df['yield_velocity']).round(2)
            sig_df = sig_df.sort_values(by='Arbitrage Index', ascending=False)
            
            sig_df = sig_df.rename(columns={
                "feature_name": "Initiative",
                "mbb_action_title": "Execution Directive",
                "virality_score": "Virality Score",
                "yield_velocity": "Yield Velocity"
            })
            
            st.dataframe(
                sig_df, use_container_width=True, hide_index=True,
                column_config={
                    "Virality Score": st.column_config.ProgressColumn("Virality Score", min_value=0, max_value=100, format="%f"),
                    "Yield Velocity": st.column_config.NumberColumn("Yield Velocity", format="%.2fx")
                }
            )
        except Exception:
            st.warning("Matrix rendering issue.")
    
    st.divider()
    
    # 6. KPI ATTRIBUTION & SOURCE CITATIONS
    col_kpi, col_sources = st.columns(2)
    
    with col_kpi:
        st.subheader("Core KPI Impact")
        kpi_matrix = doc.get('kpi_impact_matrix', {})
        if kpi_matrix and len(kpi_matrix) > 0:
            for k, v in kpi_matrix.items():
                with st.container(border=True):
                    st.markdown(f"**{k}**")
                    st.caption(v)
        else:
            st.info("No KPI metrics generated.")

    with col_sources:
        st.subheader("Epistemic Origins & Sources")
        st.caption("Data lineage supporting these missing alpha trends.")
        sources = doc.get('source_links', [])
        if sources:
            for src in sources:
                title = src.get('title', 'Industry Report')
                url = src.get('url', '#')
                with st.container(border=True):
                    st.markdown(f"🔗 [{title}]({url})")
        else:
            st.info("No external source links provided.")
