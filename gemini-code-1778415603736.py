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
# 1. TIGER ANALYTICS x KYNDRYL (SPACE EFFICIENT)
# ==========================================
st.set_page_config(page_title="Tiger Analytics | Sense & Respond OS", layout="wide")

try:
    st.logo("tiger_logo.png", icon_image="tiger_logo.png")
except Exception:
    pass

def inject_efficient_enterprise_aesthetic():
    st.markdown("""
    <style>
        /* Base Editorial Reset (Kyndryl Style) */
        html, body, [class*="css"] {
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #FAFAFA;
            color: #1C1C1C;
        }

        header[data-testid="stHeader"] {
            background-color: #FAFAFA;
            border-bottom: 2px solid #F7901D; /* Tiger Orange */
        }

        /* Lightweight Typography, Space Efficient */
        h1 { font-size: 2.2rem !important; font-weight: 300 !important; letter-spacing: -0.03em !important; color: #1C1C1C !important; padding-bottom: 0 !important; margin-bottom: 0 !important;}
        h2 { font-size: 1.4rem !important; font-weight: 400 !important; letter-spacing: -0.01em !important; color: #1C1C1C !important; margin-top: 1.5rem !important; margin-bottom: 1rem !important; border-bottom: 1px solid #E5E7EB; padding-bottom: 0.5rem;}
        h3 { font-size: 0.9rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; color: #F7901D !important; margin-bottom: 0.5rem !important; }
        p { font-size: 1rem !important; font-weight: 300 !important; line-height: 1.4 !important; }

        /* Sharp, White Containers (No Giant Black Boxes) */
        div[data-testid="stVerticalBlock"] div[style*="border"] {
            border: 1px solid #E5E7EB !important;
            border-radius: 0px !important; /* Sharp edges */
            background-color: #FFFFFF !important;
            padding: 1.25rem !important; /* Tighter padding for space efficiency */
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }

        /* Bare, Structural Metrics */
        [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 300 !important; letter-spacing: -0.03em !important; color: #1C1C1C !important; }
        [data-testid="stMetricLabel"] { font-size: 0.75rem !important; font-weight: 600 !important; text-transform: uppercase !important; color: #71717A !important; }

        /* Sharp Buttons */
        .stButton>button {
            background-color: #1C1C1C !important; color: #FFFFFF !important; border: none !important; border-radius: 0px !important;
            font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; padding: 0.5rem 1rem !important;
        }
        .stButton>button:hover { background-color: #F7901D !important; color: #1C1C1C !important; }

        /* Progress Bars */
        .stProgress > div > div > div > div { background-color: #F7901D !important; height: 6px !important; }

        /* Space Efficiency: Tighter main padding */
        .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
        .stDataFrame { border-radius: 0px !important; border: 1px solid #E5E7EB !important; }
    </style>
    """, unsafe_allow_html=True)

inject_efficient_enterprise_aesthetic()

# ==========================================
# 2. DATA ARCHITECTURE & TAXONOMY
# ==========================================
class ContextLayer(BaseModel):
    data_inventory: str
    data_directory: str
    data_registry: str
    data_dictionary: str
    metadata_repository: str

def seed_context_layer(ind: str, sub: str, per: str) -> ContextLayer:
    prefix = ind.split(' ')[0].lower()
    return ContextLayer(
        data_inventory=f"Live_API_Firehose, {sub.replace(' ', '_')}_Historical_DB",
        data_directory=f"s3://enterprise-data/{prefix}/{sub.lower().replace(' ', '_')}/",
        data_registry=f"Steward: Data_Ops | Owner: {per}",
        data_dictionary=f"Metrics tailored to {per} workflows.",
        metadata_repository="Compliance: SOC2/GDPR | Anomaly_Threshold: High"
    )

INDUSTRIES = {
    "Retail & Apparel (e.g., Nike, Gap)": ["Athleisure & Footwear", "Fast Fashion", "Luxury Apparel", "Sporting Goods"],
    "CPG & FMCG (e.g., PepsiCo)": ["Food & Beverage", "Snacks & Confectionery", "Personal Care", "Household Goods"],
    "Direct-to-Consumer (D2C)": ["Subscription Boxes", "Digital-Native Brands", "Health & Supplements"],
    "Healthcare & Life Sciences": ["Pharmaceuticals", "Medical Devices", "Consumer Health"],
    "Media & Entertainment": ["Streaming Platforms", "Gaming", "Digital Publishing"]
}

PERSONAS = [
    "Digital Marketer / Campaign App (Ops)", "Creative Designer (Ops)", "Campaign Analyst (Ops)",
    "Merchandiser / Demand Sensing (Ops)", "Data Scientist (Ops)", "Digital Product Owner (Ops)",
    "Brand Manager / War Room (Strategy)", "Chief Marketing Officer (Strategy)",
    "VP of Supply Chain & Logistics (Strategy)", "Chief Revenue Officer (Strategy)"
]

# ==========================================
# 3. SCHEMA DEFINITIONS 
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
    proactive_alert: str 
    strategic_pillars: List[Dict[str, str]]
    signals: List[StrategicSignal]
    kpi_impact_matrix: Dict[str, str]
    linchpin_risk: str
    persona_deliverables: List[Dict[str, str]]
    source_links: List[SourceLink]

# ==========================================
# 4. THE LOGIC ENGINES
# ==========================================
def simulate_external_scrape(sub_industry: str, client: Groq):
    sys_prompt = """
    You are an autonomous market anomaly detection crawler for 2026.
    Return strictly JSON with the exact keys:
    - 'market_anomaly_detected': string (Sudden competitor move, supply shock, or bleeding-edge trend).
    - 'hero_insight': 1-sentence macro trend revelation about bleeding-edge consumer demand.
    - 'sentiment_shift': string.
    - 'viral_velocity_score': integer (0-100).
    - 'trending_keywords': dictionary of 5 bleeding-edge phrases and their virality percentage (integer 1-100).
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"Scan {sub_industry}"}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return {
            "market_anomaly_detected": "Competitor launched a spatial-commerce AR integration with 40% price cuts.",
            "hero_insight": "Consumers are abandoning mass-personalization for cryptographically verified authenticity.",
            "sentiment_shift": "Consumers are exhibiting high price-sensitivity and immediate brand switching.",
            "viral_velocity_score": 92,
            "trending_keywords": {"spatial UI commerce": 100, "zero-party autonomy": 95, "neuro-aesthetic design": 90, "biophilic materials": 88, "dark-store micro-fulfillment": 80}
        }

def execute_omniverse_synthesis(ind, sub, per, context: ContextLayer, anomaly_data, client: Groq):
    action_formats = {
        "Digital Marketer / Campaign App (Ops)": "Start 'proactive_alert' with 'ALERT: [Anomaly] detected. Drafted Response Campaign:'",
        "Creative Designer (Ops)": "Start 'proactive_alert' with 'ALERT: [Anomaly] detected. Visual Pivot Required:'",
        "Campaign Analyst (Ops)": "Start 'proactive_alert' with 'ALERT: [Anomaly] detected. Budget Reallocation Plan:'",
        "Merchandiser / Demand Sensing (Ops)": "Start 'proactive_alert' with 'ALERT: [Anomaly] detected. Inventory Intervention:'",
        "Brand Manager / War Room (Strategy)": "Start 'proactive_alert' with 'ALERT: Market move detected. Strategic Counter-Positioning:'"
    }
    alert_format = action_formats.get(per, "Start 'proactive_alert' with 'ALERT: Anomaly detected.'")

    deliverable_formats = {
        "Creative Designer (Ops)": "For 'persona_deliverables', provide 3 'Pinterest-Style Sketch Prompts'. The 'image_keyword' MUST be a highly descriptive 5-7 word prompt for an AI image generator describing a physical sketch.",
        "Digital Marketer / Campaign App (Ops)": "For 'persona_deliverables', provide 3 specific 'Ad Creative Hooks'.",
        "Campaign Analyst (Ops)": "For 'persona_deliverables', provide 3 'Hyper-Targeted Experiment Hypotheses'.",
        "Merchandiser / Demand Sensing (Ops)": "For 'persona_deliverables', provide 3 'Algorithmic SKU Interventions'.",
    }
    deliv_format = deliverable_formats.get(per, "Provide 3 highly specific tactical deliverables for this persona.")

    sys_prompt = f"""
    You are an autonomous Sense & Respond Agent advising a {per} at an enterprise like Nike or PepsiCo in the {sub} ({ind}) sector.
    
    GOVERNANCE CONTEXT: {context.model_dump_json()}
    LIVE ANOMALY DETECTED: {json.dumps(anomaly_data)}

    MANDATES:
    1. {alert_format}
    2. {deliv_format}
    3. Identify the "missing alpha"—the absolute bleeding-edge trend competitors are ignoring. Do NOT use generic business fluff.

    OUTPUT FORMAT (STRICT JSON EXACTLY AS SHOWN BELOW):
    {{
        "proactive_alert": "string (The ALERT statement required above)",
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
            {{"title": "string", "url": "string"}}
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

def query_groq(prompt: str, system_context: str, client: Groq):
    try:
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are a helpful assistant refining the following strategy: {system_context}"},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant", temperature=0.5
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Chat error: {e}"

# ==========================================
# 5. STREAMLIT APP RENDERING
# ==========================================
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "scraped_data" not in st.session_state: st.session_state.scraped_data = None
if "auto_intelligence_generated" not in st.session_state: st.session_state.auto_intelligence_generated = None
if "context_layer" not in st.session_state: st.session_state.context_layer = None

st.title("Tiger Analytics | Sense & Respond OS")

st.sidebar.markdown("### Operational Parameters")
sel_ind = st.sidebar.selectbox("Industry Ecosystem", list(INDUSTRIES.keys()))
sel_sub = st.sidebar.selectbox("Sub-Industry Segment", INDUSTRIES[sel_ind])
sel_per = st.sidebar.selectbox("Autonomous Agent Persona", PERSONAS)

st.sidebar.divider()

if "GROQ_API_KEY" not in st.secrets:
    st.sidebar.error("GROQ_API_KEY missing in `.streamlit/secrets.toml`.")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if st.sidebar.button("Execute Autonomous Sequence", type="primary", use_container_width=True):
    with st.spinner("SENSE PHASE: Scanning global firehose for anomalies..."):
        ctx = seed_context_layer(sel_ind, sel_sub, sel_per)
        st.session_state.context_layer = ctx
        anomaly = simulate_external_scrape(sel_sub, client)
        st.session_state.scraped_data = anomaly
        
    with st.spinner(f"RESPOND PHASE: Generating Complete Enterprise Package for {sel_per.split(' ')[0]}..."):
        intel = execute_omniverse_synthesis(sel_ind, sel_sub, sel_per, ctx, anomaly, client)
        st.session_state.auto_intelligence_generated = intel
        st.session_state.chat_history = []

# --- MAIN DASHBOARD RENDERING ---
if st.session_state.auto_intelligence_generated:
    doc = st.session_state.auto_intelligence_generated
    sd = st.session_state.scraped_data

    if not isinstance(doc, dict):
        st.warning("🔄 System architecture updated. Please click 'Execute Autonomous Sequence' again.")
        st.stop()
    
    # --- ROW 1: ALERT & BLEEDING EDGE SIGNAL (Space Efficient Layout) ---
    col_alert, col_trends = st.columns([1.5, 1])
    
    with col_alert:
        # The Proactive Alert (No giant black box, just clean white space and sharp typography)
        st.markdown(f"<span style='color:#F7901D; font-weight:700; font-size:0.9rem; text-transform:uppercase;'>System Alert</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:1.15rem; font-weight:300; line-height:1.5; margin-bottom:1rem;'>{doc.get('proactive_alert', 'ALERT: Anomaly Detected.')}</div>", unsafe_allow_html=True)
        
        # The Restored Bleeding Edge Signal
        with st.container(border=True):
            st.markdown("### Bleeding-Edge Market Signal")
            st.markdown(f"*{sd.get('hero_insight', 'Market shift detected.')}*")
            
    with col_trends:
        # The Restored Top Trends / Progress Bars
        with st.container(border=True):
            st.markdown("### Top Trending Keywords")
            keywords = sd.get("trending_keywords", {})
            if keywords:
                for kw, score in keywords.items():
                    safe_score = min(max(int(score), 0), 100)
                    st.markdown(f"<div style='margin-bottom:-10px; font-weight:600; font-size:0.85rem;'>{kw.title()}</div>", unsafe_allow_html=True)
                    st.progress(safe_score / 100.0)
            else:
                st.caption("No keyword data available.")

    # --- ROW 2: MECE PILLARS & RISK (3 Columns) ---
    st.markdown("<h2>Actionable 'Missing Alpha' Strategy</h2>", unsafe_allow_html=True)
    pillars = doc.get('strategic_pillars', [])
    if pillars:
        cols = st.columns(len(pillars))
        for i, pillar in enumerate(pillars):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### 0{i+1} : {pillar.get('title', '').upper()}")
                    st.markdown(f"<span style='color:#49494A; font-weight:300;'>{pillar.get('description', '')}</span>", unsafe_allow_html=True)

    # --- ROW 3: EXCLUSIVE DELIVERABLES & METRICS ---
    col_deliv, col_metrics = st.columns([2, 1])
    
    with col_deliv:
        st.markdown(f"<h2>Exclusive Deliverables: {sel_per.split(' ')[0]}</h2>", unsafe_allow_html=True)
        deliverables = doc.get('persona_deliverables', [])
        if deliverables:
            del_cols = st.columns(len(deliverables))
            for i, item in enumerate(deliverables):
                with del_cols[i]:
                    d_title = item.get('title', 'Deliverable')
                    d_desc = item.get('description', 'Details pending.')
                    
                    with st.container(border=True):
                        if "Designer" in sel_per:
                            raw_kw = item.get('image_keyword', 'fashion design sketch')
                            encoded_kw = urllib.parse.quote(f"{raw_kw} pinterest style concept art sketch highly detailed clean white background")
                            img_url = f"https://image.pollinations.ai/prompt/{encoded_kw}?width=600&height=400&nologo=true"
                            # Sharp corners to match Kyndryl style
                            st.markdown(f'<img src="{img_url}" style="width: 100%; border-radius: 0px; margin-bottom: 12px;">', unsafe_allow_html=True)
                            st.markdown(f"**{d_title}**")
                        else:
                            st.markdown(f"**{d_title}**")
                        
                        st.markdown(f"<span style='color:#49494A; font-size:0.9rem; font-weight:300;'>{d_desc}</span>", unsafe_allow_html=True)

    with col_metrics:
        st.markdown("<h2>Velocity & Risk</h2>", unsafe_allow_html=True)
        st.metric("Viral Velocity Signal", f"{sd.get('viral_velocity_score', 85)}")
        with st.container(border=True):
            st.markdown("### Structural Linchpin Risk")
            st.markdown(f"<p style='color: #49494A; font-weight:300;'>{doc.get('linchpin_risk', 'N/A')}</p>", unsafe_allow_html=True)

    # --- ROW 4: ARBITRAGE MATRIX ---
    st.markdown("<h2>Initiative Prioritization & Arbitrage</h2>", unsafe_allow_html=True)
    signals = doc.get('signals', [])
    if signals:
        try:
            sig_df = pd.DataFrame(signals)
            sig_df['Arbitrage Index'] = (sig_df['virality_score'] * sig_df['yield_velocity']).round(2)
            sig_df = sig_df.sort_values(by='Arbitrage Index', ascending=False)
            sig_df = sig_df.rename(columns={"feature_name": "Initiative", "mbb_action_title": "Execution Directive", "virality_score": "Virality Score", "yield_velocity": "Yield Velocity"})
            st.dataframe(sig_df, use_container_width=True, hide_index=True)
        except Exception:
            st.warning("Matrix rendering issue.")
            
    # --- ROW 5: KPI & SOURCES ---
    col_kpi, col_sources = st.columns(2)
    with col_kpi:
        st.markdown("<h2>Core KPI Impact</h2>", unsafe_allow_html=True)
        kpi_matrix = doc.get('kpi_impact_matrix', {})
        if kpi_matrix:
            for k, v in kpi_matrix.items():
                with st.container(border=True):
                    st.markdown(f"**{k}**")
                    st.markdown(f"<span style='color:#49494A; font-weight:300;'>{v}</span>", unsafe_allow_html=True)
                    
    with col_sources:
        st.markdown("<h2>Epistemic Origins & Sources</h2>", unsafe_allow_html=True)
        sources = doc.get('source_links', [])
        if sources:
            for src in sources:
                with st.container(border=True):
                    st.markdown(f"🔗 [{src.get('title', 'Source')}]({src.get('url', '#')})")

    # --- ROW 6: RAW DATA EXPANDER ---
    with st.expander("View Raw Sense Engine Data & Governance Artifacts", expanded=False):
        st.json(sd)
        st.code(st.session_state.context_layer.model_dump_json(indent=2), language="json")

    st.divider()

    # --- ROW 7: CHAT ---
    st.markdown("<h2>Human-in-the-Loop Refinement</h2>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
            
    if prompt := st.chat_input("Refine the strategy, adjust tone, or approve..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Refining..."):
                response = query_groq(prompt=prompt, system_context=json.dumps(doc), client=client)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

    # --- FOOTER ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: left; color: #71717A; font-size: 0.8rem; font-weight: 600; border-top: 1px solid #E5E7EB; padding-top: 1.5rem; text-transform: uppercase; letter-spacing: 0.05em;'>
            © 2022 - 2026, Tiger Analytics Inc. All rights reserved.<br>
            <span style='font-weight: 300; letter-spacing: 0;'>Powered by Experience Consulting Team</span>
        </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left; font-size: 2.8rem !important; margin-top: 0 !important; color: #1C1C1C !important; font-weight: 300 !important; letter-spacing: -0.04em;'>Welcome to the Sense & Respond OS.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; font-weight: 300; color: #49494A; max-width: 700px;'>Configure your operational parameters in the sidebar and execute the autonomous sequence to detect real-time anomalies and trigger agentic response workflows.</p>", unsafe_allow_html=True)
