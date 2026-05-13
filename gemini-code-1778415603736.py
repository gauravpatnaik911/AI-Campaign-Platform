import streamlit as st
import json
import pandas as pd
import urllib.parse
import os
from pydantic import BaseModel
from typing import List, Dict

# --- CORE LIBRARY CHECK ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. Run: pip install groq")
    st.stop()

# ==========================================
# 1. TIGER ANALYTICS BRANDING & UI INJECTION
# ==========================================
st.set_page_config(page_title="Tiger Analytics | Sense & Respond OS", layout="wide", page_icon="🐅")

# Logo Integration (Ensure 'tiger_logo.png' is in your repo)
try:
    st.logo("tiger_logo.png", icon_image="tiger_logo.png")
except Exception:
    pass # Fails gracefully if the logo isn't uploaded yet

def inject_tiger_aesthetic():
    st.markdown("""
    <style>
        /* Base Typography & Background */
        html, body, [class*="css"] {
            font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #FFFFFF;
            color: #1C1C1C; /* Tiger Primary Dark */
        }
        
        /* Change the top header line to Tiger Analytics Orange */
        header[data-testid="stHeader"] {
            background-color: #FFFFFF;
            border-bottom: 4px solid #F7901D; /* Tiger Primary Orange */
        }
        
        /* Top-Down Hierarchy Headers */
        h1 { font-weight: 800; border-bottom: 3px solid #F7901D; padding-bottom: 10px; color: #1C1C1C !important; }
        h2 { font-weight: 700; color: #1C1C1C !important; border-left: 6px solid #F7901D; padding-left: 12px; margin-top: 1.5rem !important; }
        h3 { font-weight: 600; color: #49494A !important; } /* Tiger Primary Grey */

        /* Brand the buttons */
        .stButton>button {
            background-color: #1C1C1C !important;
            color: #FFFFFF !important;
            border: 1px solid #1C1C1C !important;
            border-radius: 4px !important;
            font-weight: 700 !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease-in-out !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .stButton>button:hover {
            background-color: #F7901D !important;
            color: #1C1C1C !important;
            border-color: #F7901D !important;
            box-shadow: 0 4px 10px rgba(247, 144, 29, 0.3) !important;
            transform: translateY(-2px);
        }

        /* Metrics & Containers */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E2E2; /* Muted Grey */
            border-radius: 4px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-top: 4px solid #18749C; /* Tiger Secondary Blue */
        }
        
        /* Alerts & Info Boxes */
        .stAlert { border-left: 5px solid #F7901D !important; background-color: #FFF9F2 !important; color: #1C1C1C !important;}
        .stInfo { border-left: 5px solid #02C2A2 !important; } /* Tiger Secondary Teal */
        
        /* Progress Bars */
        .stProgress > div > div > div > div { background-color: #F7901D !important; }

        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

inject_tiger_aesthetic()

# ==========================================
# 2. DATA ARCHITECTURE & GOVERNANCE
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

# ==========================================
# 3. SCALED ENTERPRISE TAXONOMY
# ==========================================
INDUSTRIES = {
    "Retail & Apparel (e.g., Nike, Gap)": ["Athleisure & Footwear", "Fast Fashion", "Luxury Apparel", "Sporting Goods"],
    "CPG & FMCG (e.g., PepsiCo)": ["Food & Beverage", "Snacks & Confectionery", "Personal Care", "Household Goods"],
    "Direct-to-Consumer (D2C)": ["Subscription Boxes", "Digital-Native Brands", "Health & Supplements"],
    "Healthcare & Life Sciences": ["Pharmaceuticals", "Medical Devices", "Consumer Health"],
    "Media & Entertainment": ["Streaming Platforms", "Gaming", "Digital Publishing"]
}

PERSONAS = [
    "Digital Marketer / Campaign App (Ops)",
    "Creative Designer (Ops)",
    "Campaign Analyst (Ops)",
    "Merchandiser / Demand Sensing (Ops)",
    "Data Scientist (Ops)",
    "Digital Product Owner (Ops)",
    "Brand Manager / War Room (Strategy)",
    "Chief Marketing Officer (Strategy)",
    "VP of Supply Chain & Logistics (Strategy)",
    "Chief Revenue Officer (Strategy)"
]

# ==========================================
# 4. SCHEMA DEFINITIONS 
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
# 5. THE LOGIC ENGINES
# ==========================================
def simulate_external_scrape(sub_industry: str, client: Groq):
    sys_prompt = """
    You are an autonomous market anomaly detection crawler for 2026.
    Return strictly JSON with the exact keys:
    - 'market_anomaly_detected': string (Sudden competitor move, supply shock, or bleeding-edge trend).
    - 'sentiment_shift': string.
    - 'viral_velocity_score': integer (0-100).
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"Scan {sub_industry}"}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return {
            "market_anomaly_detected": "Competitor unexpectedly launched a spatial-commerce AR integration with 40% price cuts.",
            "sentiment_shift": "Consumers are exhibiting high price-sensitivity and immediate brand switching.",
            "viral_velocity_score": 92
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
            {{"title": "string (e.g., Gartner, Business of Fashion)", "url": "string"}}
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
            model="llama-3.1-8b-instant",
            temperature=0.5
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Chat error: {e}"

# ==========================================
# 6. STREAMLIT APP RENDERING
# ==========================================

# --- STATE MANAGEMENT ---
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "scraped_data" not in st.session_state: st.session_state.scraped_data = None
if "auto_intelligence_generated" not in st.session_state: st.session_state.auto_intelligence_generated = None
if "context_layer" not in st.session_state: st.session_state.context_layer = None

# --- MAIN TITLE ---
st.title("🐅 Tiger Analytics | Sense & Respond OS")

# --- SIDEBAR CONTROLS ---
st.sidebar.title("⚡ Marketing OS")
sel_ind = st.sidebar.selectbox("Industry Ecosystem", list(INDUSTRIES.keys()))
sel_sub = st.sidebar.selectbox("Sub-Industry Segment", INDUSTRIES[sel_ind])
sel_per = st.sidebar.selectbox("Autonomous Agent Persona", PERSONAS)

st.sidebar.divider()

if "GROQ_API_KEY" not in st.secrets:
    st.sidebar.error("GROQ_API_KEY missing in `.streamlit/secrets.toml`.")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if st.sidebar.button("Run Sense & Respond Sequence", type="primary", use_container_width=True):
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
        st.warning("🔄 System architecture has been updated. Please click 'Run Sense & Respond Sequence' again to sync the new data format.")
        st.stop()
    
    # 1. RAW DATA EXPANDER
    with st.expander("📡 View Raw Sense Engine Data & Governance Artifacts", expanded=False):
        st.json(sd)
        st.markdown("**Active Governance Artifacts Enforced:**")
        st.code(st.session_state.context_layer.model_dump_json(indent=2), language="json")

    # 2. THE PROACTIVE ALERT
    st.info("System generated proactive response:")
    with st.container(border=True):
        st.markdown(f"**{doc.get('proactive_alert', 'ALERT: Anomaly Detected.')}**")

    st.divider()
    
    # 3. VELOCITY & RISK
    col_vel, col_risk = st.columns(2)
    with col_vel:
        st.metric("Viral Velocity of Anomaly", f"{sd.get('viral_velocity_score', 85)} / 100")
    with col_risk:
        st.error(f"**Linchpin Risk:** {doc.get('linchpin_risk', 'N/A')}")
        
    st.divider()

    # 4. MECE PILLARS (Missing Alpha)
    st.subheader(f"Actionable 'Missing Alpha' Strategy")
    pillars = doc.get('strategic_pillars', [])
    if pillars:
        cols = st.columns(len(pillars))
        for i, pillar in enumerate(pillars):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"#### 0{i+1}")
                    st.markdown(f"**{pillar.get('title', '')}**")
                    st.markdown(f"<span style='color:#49494A'>{pillar.get('description', '')}</span>", unsafe_allow_html=True)

    st.divider()

    # 5. EXCLUSIVE PERSONA DELIVERABLES (PINTEREST GENERATOR)
    st.subheader(f"Exclusive Deliverables: {sel_per.split(' ')[0]}")
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
                        st.markdown(f'<img src="{img_url}" style="width: 100%; border-radius: 4px; margin-bottom: 12px; border: 1px solid #E2E2E2;">', unsafe_allow_html=True)
                        st.markdown(f"**Visual Concept: {d_title}**")
                    else:
                        st.markdown(f"**Tactical Asset: {d_title}**")
                    
                    st.markdown(f"<span style='color:#49494A'>{d_desc}</span>", unsafe_allow_html=True)
    else:
        st.info(f"No specific tactical deliverables generated for {sel_per}.")

    st.divider()

    # 6. ARBITRAGE MATRIX (Now matching the Orange/Grey Data Viz Brand logic)
    st.subheader("Initiative Prioritization & Arbitrage")
    signals = doc.get('signals', [])
    if signals:
        try:
            sig_df = pd.DataFrame(signals)
            sig_df['Arbitrage Index'] = (sig_df['virality_score'] * sig_df['yield_velocity']).round(2)
            sig_df = sig_df.sort_values(by='Arbitrage Index', ascending=False)
            sig_df = sig_df.rename(columns={"feature_name": "Initiative", "mbb_action_title": "Execution Directive", "virality_score": "Virality Score", "yield_velocity": "Yield Velocity"})
            st.dataframe(
                sig_df.style.background_gradient(subset=['Arbitrage Index'], cmap='Oranges'), 
                use_container_width=True, hide_index=True
            )
        except Exception:
            st.warning("Matrix rendering issue.")
            
    st.divider()
    
    # 7. KPI & SOURCES
    col_kpi, col_sources = st.columns(2)
    with col_kpi:
        st.subheader("Core KPI Impact")
        kpi_matrix = doc.get('kpi_impact_matrix', {})
        if kpi_matrix:
            for k, v in kpi_matrix.items():
                with st.container(border=True):
                    st.markdown(f"**{k}**")
                    st.caption(v)
                    
    with col_sources:
        st.subheader("Epistemic Origins & Sources")
        sources = doc.get('source_links', [])
        if sources:
            for src in sources:
                with st.container(border=True):
                    st.markdown(f"🔗 [{src.get('title', 'Source')}]({src.get('url', '#')})")

    st.divider()

    # 8. HUMAN-IN-THE-LOOP CHAT
    st.markdown("### 💬 Human-in-the-Loop Refinement")
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

    # --- TIGER ANALYTICS OFFICIAL FOOTER ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: #49494A; font-size: 0.85rem; border-top: 1px solid #E2E2E2; padding-top: 20px;'>
            © 2022 - 2023, Tiger Analytics Inc; All rights reserved.<br>
            <i>Powered by Experience Consulting Team</i>
        </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("### Welcome to the Sense & Respond OS")
    st.write("👈 Configure your parameters and click **Run Sense & Respond Sequence** to trigger an autonomous agent.")
