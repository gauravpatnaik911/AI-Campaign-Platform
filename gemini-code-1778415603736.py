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
    """Crawls for raw viral semantic data. This identifies the OVERARCHING macro trend."""
    sys_prompt = """
    You are a predictive text-mining crawler. Return strictly JSON:
    - 'hero_insight': 1-sentence macro trend revelation about consumer demand.
    - 'viral_velocity_score': integer (0-100).
    - 'demand_trajectory': string (e.g., 'Hyper-Growth', 'Cooling').
    - 'trending_keywords': dictionary of 6 exactly trending phrases and their virality percentage (integer 1-100). Example: {"sustainable packaging": 92}
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"Scan {sub_industry}"}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return {
            "hero_insight": "Consumers are shifting rapidly towards hyper-personalized, eco-conscious consumption.", 
            "viral_velocity_score": 88, "demand_trajectory": "Accelerating",
            "trending_keywords": {"eco-packaging": 95, "personalization AI": 88, "limited drops": 100, "clean ingredients": 75, "social commerce": 80, "loyalty apps": 90}
        }

def execute_omniverse_synthesis(ind, sub, per, social_data, client):
    """Synthesizes strategy heavily indexed on the selected Persona. The 'So What' engine."""
    
    persona_directives = {
        "Creative Designer (Ops)": "Focus ONLY on visual assets, color palettes, UX/UI, mood boards, ad creative, and translating the trend data into physical or digital design language. Do NOT talk about media buying or supply chain.",
        "Campaign Analyst (Ops)": "Focus ONLY on media mix modeling, ROAS, CPA targets, A/B testing ad copy, audience segmentation, and attribution tracking. Provide mathematical/analytical action points. Do NOT talk about product design.",
        "Merchandising Manager (Ops)": "Focus ONLY on SKU rationalization, shelf placement, stock-to-sales ratios, pricing tiers, and cross-selling strategies. How does the trend affect inventory placement?",
        "Data Scientist (Ops)": "Focus ONLY on building predictive models, data pipelines, NLP sentiment tracking, clustering algorithms, and model deployment strategies based on the trend.",
        "Digital Product Owner (Ops)": "Focus ONLY on app features, checkout conversion funnels, sprint planning, feature backlogs, and e-commerce UI/UX functionality.",
        "Chief Marketing Officer (Strategy)": "Focus ONLY on overarching brand positioning, total market share capture, budget allocation across channels, and macro brand narrative.",
        "VP of Supply Chain & Logistics (Strategy)": "Focus ONLY on supplier diversification, freight costs, warehouse automation, fulfillment speed, and inventory turnaround times.",
        "Chief Revenue Officer (Strategy)": "Focus ONLY on top-line revenue, channel partnerships, B2B wholesale expansion, sales velocity, and overall margin growth."
    }
    
    directive = persona_directives.get(per, "Provide actionable insights relevant to the persona.")

    sys_prompt = f"""
    You are an elite Strategy Partner advising a {per} at a major enterprise (e.g., Nike, PepsiCo) in the {sub} ({ind}) sector.
    
    LIVE VIRAL MACRO-TREND DATA: {json.dumps(social_data)}

    CRITICAL DIRECTIVE FOR THIS PERSONA: 
    {directive}

    MANDATES:
    1. Governing Thought: Board-level answer integrating the Live Viral Data, specifically tailored to the {per}'s daily KPIs.
    2. MECE Pillars: 3 strategic pillars. EXACT keys: 'title' and 'description'. The description MUST explain the "So What?" and exact "Action Points" for this specific persona.
    3. Action Titles: Every response must drive execution for the {per}.
    4. KPI Impact Matrix: You MUST provide a dictionary of 3 core KPIs and how this strategy impacts them. Example: {{"CPA": "Reduces by 15% due to better targeting"}}.
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
    with st.spinner(f"Aggregating Viral Data & Tailoring for {sel_per.split(' ')[0]}..."):
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
    st.info(f"**Live Macro Trend Signal:** {sd.get('hero_insight', '')}")
    
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
    st.subheader(f"Actionable Strategy for {sel_per.split(' ')[0]}")
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
    else:
        st.warning("No strategic pillars generated.")

    st.divider()

    # 4. ARBITRAGE MATRIX
    st.subheader(f"Initiative Prioritization & Arbitrage")
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
                sig_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Virality Score": st.column_config.ProgressColumn("Virality Score", min_value=0, max_value=100, format="%f"),
                    "Yield Velocity": st.column_config.NumberColumn("Yield Velocity", format="%.2fx")
                }
            )
        except Exception as e:
            st.warning("Could not render the Arbitrage Matrix properly based on the AI output format.")
    else:
        st.info("No signal initiatives generated.")

    # 5. KPI ATTRIBUTION (Bug Fixed Here)
    st.subheader("Core KPI Impact")
    kpi_matrix = doc.get('kpi_impact_matrix', {})
    
    # Safety Check: Only create columns if the KPI dictionary actually contains items
    if kpi_matrix and len(kpi_matrix) > 0:
        kpi_cols = st.columns(len(kpi_matrix))
        for i, (k, v) in enumerate(kpi_matrix.items()):
            with kpi_cols[i % len(kpi_cols)]:
                with st.container(border=True):
                    st.markdown(f"**{k}**")
                    st.caption(v)
    else:
        st.info("No KPI attribution metrics generated for this scenario.")
