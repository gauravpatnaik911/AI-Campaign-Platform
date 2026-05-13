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
# 1. TIGER ANALYTICS UI SETTINGS
# ==========================================
st.set_page_config(page_title="Tiger Analytics | Sense & Respond OS", layout="wide")

try:
    st.logo("tiger_logo.png", icon_image="tiger_logo.png")
except Exception:
    pass

def inject_efficient_enterprise_aesthetic():
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #FAFAFA;
            color: #1C1C1C;
        }
        header[data-testid="stHeader"] { background-color: #FAFAFA; border-bottom: 2px solid #F7901D; }
        h1 { font-size: 2.2rem !important; font-weight: 300 !important; letter-spacing: -0.03em !important; color: #1C1C1C !important; padding-bottom: 0 !important; margin-bottom: 0 !important;}
        h2 { font-size: 1.4rem !important; font-weight: 400 !important; letter-spacing: -0.01em !important; color: #1C1C1C !important; margin-top: 1.5rem !important; margin-bottom: 1rem !important; border-bottom: 1px solid #E5E7EB; padding-bottom: 0.5rem;}
        h3 { font-size: 0.9rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; color: #F7901D !important; margin-bottom: 0.5rem !important; }
        
        div[data-testid="stVerticalBlock"] div[style*="border"] {
            border: 1px solid #E5E7EB !important; border-radius: 0px !important; 
            background-color: #FFFFFF !important; padding: 1.25rem !important; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }

        .stButton>button {
            background-color: #1C1C1C !important; color: #FFFFFF !important; border: none !important; border-radius: 0px !important;
            font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; padding: 0.5rem 1rem !important;
        }
        .stButton>button:hover { background-color: #F7901D !important; color: #1C1C1C !important; }
        .stProgress > div > div > div > div { background-color: #F7901D !important; height: 6px !important; }
        .stChatMessage { background-color: #FFFFFF !important; border: 1px solid #E5E7EB !important; border-radius: 4px !important; padding: 1rem !important; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
        
        /* Metric Styling for McKinsey KPIs */
        [data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 300 !important; color: #1C1C1C !important; }
        [data-testid="stMetricLabel"] { font-size: 0.8rem !important; font-weight: 700 !important; text-transform: uppercase !important; color: #F7901D !important; }
    </style>
    """, unsafe_allow_html=True)

inject_efficient_enterprise_aesthetic()

# ==========================================
# 2. DATA ARCHITECTURE & TAXONOMY (Refined to 5)
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
    "Creative Designer (Ops)", 
    "Campaign Analyst (Ops)", 
    "Merchandiser / Demand Sensing (Ops)", 
    "Chief Marketing Officer (Strategy)", 
    "VP of Supply Chain & Logistics (Strategy)"
]

# ==========================================
# 3. SCHEMA DEFINITIONS (Arbitrage Removed)
# ==========================================
class SourceLink(BaseModel):
    title: str
    url: str

class KPIImpact(BaseModel):
    kpi_name: str
    impact_metric: str
    mckinsey_rationale: str

class OmniverseIntelligence(BaseModel):
    proactive_alert: str 
    trend_implication: str
    strategic_pillars: List[Dict[str, str]]
    kpi_impact_matrix: List[KPIImpact] 
    persona_deliverables: List[Dict[str, str]]
    source_links: List[SourceLink]

# ==========================================
# 4. THE LOGIC ENGINES
# ==========================================
def simulate_external_scrape(sub_industry: str, client: Groq):
    sys_prompt = """
    You are an autonomous market anomaly crawler for 2026.
    Return strictly JSON with the exact keys:
    - 'hero_insight': 1-sentence macro trend revelation about bleeding-edge consumer demand.
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
            "hero_insight": "Consumers are abandoning mass-personalization for cryptographically verified authenticity.",
            "trending_keywords": {"spatial UI commerce": 100, "zero-party autonomy": 95, "neuro-aesthetic design": 90, "biophilic materials": 88, "dark-store micro-fulfillment": 80}
        }

def execute_omniverse_synthesis(ind, sub, per, context: ContextLayer, anomaly_data, client: Groq):
    
    deliverable_formats = {
        "Creative Designer (Ops)": "For 'persona_deliverables', provide 3 'Pinterest-Style Sketch Prompts' that directly execute your pillars. The 'image_keyword' MUST be a highly descriptive 5-7 word prompt for an AI image generator describing a physical sketch.",
        "Campaign Analyst (Ops)": "For 'persona_deliverables', provide 3 'Hyper-Targeted Experiment Hypotheses' that directly execute your pillars.",
        "Merchandiser / Demand Sensing (Ops)": "For 'persona_deliverables', provide 3 'Algorithmic SKU Interventions' that directly execute your pillars.",
        "Chief Marketing Officer (Strategy)": "For 'persona_deliverables', provide 3 'Macro Brand Repositioning Briefs' that directly execute your pillars.",
        "VP of Supply Chain & Logistics (Strategy)": "For 'persona_deliverables', provide 3 'Logistics Resiliency Blueprints' that directly execute your pillars."
    }
    deliv_format = deliverable_formats.get(per, "Provide 3 highly functional tactical assets.")

    sys_prompt = f"""
    You are an autonomous Agent advising a {per} at an enterprise like Nike or PepsiCo in the {sub} ({ind}) sector.
    
    GOVERNANCE CONTEXT: {context.model_dump_json()}
    LIVE MACRO TREND DATA: {json.dumps(anomaly_data)}

    MANDATES:
    1. Identify the "missing alpha"—the absolute bleeding-edge trend competitors are ignoring. 
    2. {deliv_format}
    3. The 'trend_implication' explicitly explains the "So What?"—why these specific virality keywords matter right now to the business bottom line.
    4. For the 'kpi_impact_matrix', the 'mckinsey_rationale' must read like a McKinsey consultant explaining the structural economic drivers behind the metric change. Do not just say "sales go up". Explain the lever.

    OUTPUT FORMAT (STRICT JSON EXACTLY AS SHOWN BELOW):
    {{
        "proactive_alert": "string (Start with 'ALERT: [Anomaly] detected.')",
        "trend_implication": "string (Detailed explanation of why these keywords are trending and the immediate business implication)",
        "strategic_pillars": [
            {{"title": "string", "description": "string (Exact execution instructions)"}},
            {{"title": "string", "description": "string"}},
            {{"title": "string", "description": "string"}}
        ],
        "kpi_impact_matrix": [
            {{"kpi_name": "string (e.g., CAC, Margin)", "impact_metric": "string (e.g., -15%)", "mckinsey_rationale": "string (McKinsey-style economic rationale)"}}
        ],
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

st.title("Tiger Analytics | OS")

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
        
    with st.spinner(f"RESPOND PHASE: Generating {sel_per.split(' ')[0]} Package..."):
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

    # 1. HERO INSIGHT
    st.markdown(f"<div style='font-size:1.15rem; font-weight:300; line-height:1.5; color:#1C1C1C; padding: 1rem 0; border-bottom: 1px solid #E5E7EB; margin-bottom: 1.5rem;'><strong>Bleeding-Edge Signal:</strong> {sd.get('hero_insight', 'Market shift detected.')}</div>", unsafe_allow_html=True)

    # 2. TRENDS & THE "SO WHAT"
    col_trends, col_implication = st.columns([1, 1.5])
    
    with col_trends:
        with st.container(border=True):
            st.markdown("### Top Trending Signals")
            keywords = sd.get("trending_keywords", {})
            if keywords:
                for kw, score in keywords.items():
                    safe_score = min(max(int(score), 0), 100)
                    st.markdown(f"<div style='margin-bottom:-10px; font-weight:600; font-size:0.85rem;'>{kw.title()} <span style='float:right; color:#F7901D;'>{safe_score}%</span></div>", unsafe_allow_html=True)
                    st.progress(safe_score / 100.0)
            else:
                st.caption("No keyword data available.")

    with col_implication:
        with st.container(border=True):
            st.markdown("### The 'So What?' (Virality Implication)")
            st.markdown(f"<span style='color:#49494A; font-size:1rem; font-weight:300; line-height:1.6;'>{doc.get('trend_implication', 'Detailed business implication pending...')}</span>", unsafe_allow_html=True)

    # 3. MECE PILLARS 
    st.markdown("<h2>Actionable Strategy</h2>", unsafe_allow_html=True)
    pillars = doc.get('strategic_pillars', [])
    if pillars:
        cols = st.columns(len(pillars))
        for i, pillar in enumerate(pillars):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### 0{i+1} : {pillar.get('title', '').upper()}")
                    st.markdown(f"<span style='color:#49494A; font-size:0.95rem; font-weight:300;'>{pillar.get('description', '')}</span>", unsafe_allow_html=True)

    # 4. CHAT BOX
    st.markdown("""
        <div style="background-color: #FFF9F2; border-left: 4px solid #F7901D; padding: 1.5rem; margin-top: 3rem; margin-bottom: 1rem;">
            <h2 style="margin-top: 0 !important; border: none !important;">💬 Human-in-the-Loop Refinement</h2>
            <p style="margin: 0; color: #49494A; font-weight: 300;">Interact with the Agent below to adjust parameters, alter the tone, or approve the strategy before moving to execution deliverables.</p>
        </div>
    """, unsafe_allow_html=True)
    
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

    st.divider()

    # 5. FUNCTIONAL DELIVERABLES 
    st.markdown(f"<h2>Functional Execution Assets: {sel_per.split(' ')[0]}</h2>", unsafe_allow_html=True)
    st.caption("Directly tied to executing the strategy pillars above.")
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
                        st.markdown(f'<img src="{img_url}" style="width: 100%; border-radius: 0px; margin-bottom: 1rem;">', unsafe_allow_html=True)
                        st.markdown(f"**Visual Concept: {d_title}**")
                    else:
                        st.markdown(f"**{d_title}**")
                    
                    st.markdown(f"<span style='color:#49494A; font-size:0.9rem; font-weight:300;'>{d_desc}</span>", unsafe_allow_html=True)

    st.divider()
    
    # 6. KPI IMPACT (Dynamically hides for Creative Designer) & SOURCES
    col_kpi, col_sources = st.columns(2)
    
    with col_kpi:
        if "Designer" not in sel_per:
            st.markdown("<h2>Core KPI Impact & Rationale</h2>", unsafe_allow_html=True)
            kpi_matrix = doc.get('kpi_impact_matrix', [])
            if kpi_matrix:
                for kpi in kpi_matrix:
                    with st.container(border=True):
                        st.metric(kpi.get('kpi_name', 'KPI'), kpi.get('impact_metric', '0%'))
                        st.markdown(f"<span style='color:#49494A; font-size:0.95rem; font-weight:300; line-height:1.5;'>{kpi.get('mckinsey_rationale', '')}</span>", unsafe_allow_html=True)
        else:
             st.markdown("")

    with col_sources:
        st.markdown("<h2>Epistemic Origins & Sources</h2>", unsafe_allow_html=True)
        sources = doc.get('source_links', [])
        if sources:
            for src in sources:
                with st.container(border=True):
                    st.markdown(f"🔗 [{src.get('title', 'Source')}]({src.get('url', '#')})")

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
