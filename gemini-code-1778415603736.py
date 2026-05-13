import streamlit as st
import json
from pydantic import BaseModel
from typing import List, Dict

# --- INSTITUTIONAL LIBRARY CHECK ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. Run: pip install groq")
    st.stop()

# ==========================================
# STEP 1: DATA ARCHITECTURE & TYPES
# ==========================================
class ContextLayer(BaseModel):
    data_inventory: str
    data_directory: str
    data_registry: str
    data_dictionary: str
    metadata_repository: str

# ==========================================
# STEP 2: SCALED ENTERPRISE TAXONOMY
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

def seed_context_layer(ind: str, sub: str, per: str) -> ContextLayer:
    """Generates mock enterprise governance artifacts based on selections."""
    prefix = ind.split(' ')[0].lower()
    return ContextLayer(
        data_inventory=f"Live_API_Firehose, {sub.replace(' ', '_')}_Historical_DB",
        data_directory=f"s3://enterprise-data/{prefix}/{sub.lower().replace(' ', '_')}/",
        data_registry=f"Steward: Data_Ops | Owner: {per}",
        data_dictionary=f"Metrics strictly tailored to {per} workflows.",
        metadata_repository="Compliance: SOC2/GDPR | Anomaly_Threshold: High"
    )

# ==========================================
# STEP 3: SYNTHETIC SENSE ENGINE
# ==========================================
def simulate_external_scrape(sub_industry: str, client: Groq):
    """SENSE PHASE: Simulates a real-time market anomaly using strict JSON."""
    sys_prompt = """
    You are an autonomous market anomaly detection crawler operating in 2026.
    Return strictly JSON with the following exact keys:
    - 'market_anomaly_detected': string (Describe a sudden, highly specific external event, competitor move, supply shock, or viral trend).
    - 'sentiment_shift': string (Describe how consumer or market sentiment has shifted in the last 24 hours).
    """
    try:
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": sys_prompt}, 
                {"role": "user", "content": f"Scan real-time market signals for {sub_industry}."}
            ],
            model="llama-3.3-70b-versatile", 
            response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {
            "market_anomaly_detected": "Major competitor unexpectedly slashed prices by 40% across flagship product lines while launching a massive TikTok takeover.",
            "sentiment_shift": "Consumers are exhibiting high price-sensitivity and immediate brand switching behaviors."
        }

# ==========================================
# STEP 4: LLM ORCHESTRATION (RESPOND ENGINE)
# ==========================================
def generate_proactive_response(ind, sub, per, context: ContextLayer, anomaly_data, client: Groq):
    """RESPOND PHASE: Generates proactive, persona-specific strategy alerts."""
    
    # ---------------------------------------------------------
    # DYNAMIC AGENTIC ROUTER (10 Personas)
    # ---------------------------------------------------------
    action_formats = {
        "Digital Marketer / Campaign App (Ops)": "Must start with 'ALERT: [Insert Anomaly] detected. Drafted Response Campaign:' Followed by targeted demographic segment, exact email copy, and a TikTok hook.",
        "Creative Designer (Ops)": "Must start with 'ALERT: [Insert Anomaly] detected. Visual Pivot Required:' Followed by exact design asset updates, color palette shifts, and moodboard direction.",
        "Campaign Analyst (Ops)": "Must start with 'ALERT: [Insert Anomaly] detected. Budget Reallocation Plan:' Followed by A/B test parameters, CPA impact predictions, and media mix adjustments.",
        "Merchandiser / Demand Sensing (Ops)": "Must start with 'ALERT: [Insert Anomaly] detected. Inventory Intervention:' Followed by projected stock-to-sales shifts and exact SKU rationalization/allocation advice.",
        "Data Scientist (Ops)": "Must start with 'ALERT: [Insert Anomaly] detected. Model Drift Warning:' Followed by required algorithm recalibrations, synthetic data generation needs, or pipeline adjustments.",
        "Digital Product Owner (Ops)": "Must start with 'ALERT: [Insert Anomaly] detected. Feature Sprint Adjustment:' Followed by UI/UX backlog prioritization and checkout funnel optimizations.",
        "Brand Manager / War Room (Strategy)": "Must start with 'ALERT: Competitor/Market move detected. Strategic Counter-Positioning:' Followed by brand voice guidelines and rapid differentiation tactics.",
        "Chief Marketing Officer (Strategy)": "Must start with 'ALERT: Macro Anomaly detected. Board-Level Marketing Pivot:' Followed by overarching positioning, market share defense, and high-level budget reallocation.",
        "VP of Supply Chain & Logistics (Strategy)": "Must start with 'ALERT: Supply/Demand Shock detected. Logistics Countermeasure:' Followed by freight, warehousing, supplier diversification, and fulfillment routing changes.",
        "Chief Revenue Officer (Strategy)": "Must start with 'ALERT: Revenue Threat/Opportunity detected. Monetization Pivot:' Followed by pricing elasticity adjustments, B2B/B2C channel shifts, and margin defense."
    }
    
    action_format = action_formats.get(per, "Must start with 'ALERT: Anomaly detected.' Followed by strategic advice.")

    sys_prompt = f"""
    You are an autonomous Sense & Respond Agent acting as a {per} in the {sub} ({ind}) sector.
    
    GOVERNANCE CONTEXT: {context.json()}
    LIVE ANOMALY DETECTED: {json.dumps(anomaly_data)}

    MANDATE:
    You must draft an immediate, proactive response to the anomaly tailored EXACTLY to the {per}'s daily KPIs.
    
    CRITICAL FORMATTING RULE: 
    {action_format}
    
    Do not include conversational filler. Be highly technical, precise, and ready for executive review. Use markdown for readability.
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama-3.3-70b-versatile", 
            temperature=0.3 
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error generating proactive response: {e}"

def query_groq(prompt: str, system_context: str, client: Groq):
    """Handles Human-in-the-Loop chat queries."""
    try:
        resp = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are a helpful assistant refining the following strategy: {system_context}"},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant", # Faster model for chat interactivity
            temperature=0.5
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Chat error: {e}"

# ==========================================
# STEP 5: STREAMLIT FRONTEND
# ==========================================
st.set_page_config(page_title="Sense & Respond OS", layout="wide")

# Minimalist Native UI CSS
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1, h2, h3 { font-weight: 800; color: #0f172a;}
        .stAlert { border-left: 5px solid #3b82f6 !important; }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scraped_data" not in st.session_state:
    st.session_state.scraped_data = None
if "auto_intelligence_generated" not in st.session_state:
    st.session_state.auto_intelligence_generated = None
if "context_layer" not in st.session_state:
    st.session_state.context_layer = None

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
    with st.spinner("SENSE PHASE: Scanning global firehose for market anomalies..."):
        # 1. Seed Governance
        ctx = seed_context_layer(sel_ind, sel_sub, sel_per)
        st.session_state.context_layer = ctx
        
        # 2. Sense Engine
        anomaly = simulate_external_scrape(sel_sub, client)
        st.session_state.scraped_data = anomaly
        
    with st.spinner(f"RESPOND PHASE: Drafting proactive intelligence for {sel_per.split(' ')[0]}..."):
        # 3. Respond Engine
        alert = generate_proactive_response(sel_ind, sel_sub, sel_per, ctx, anomaly, client)
        st.session_state.auto_intelligence_generated = alert
        
        # Clear chat history on new run
        st.session_state.chat_history = []

# --- MAIN DASHBOARD RENDERING ---
if st.session_state.auto_intelligence_generated:
    st.markdown(f"### Autonomous Intelligence: {sel_per.split('(')[0]}")
    
    # Render Simulated Anomaly in an Expander
    with st.expander("📡 View Raw Sense Engine Data & Governance Artifacts", expanded=False):
        st.markdown("**Simulated Market Anomaly (JSON):**")
        st.json(st.session_state.scraped_data)
        st.markdown("**Active Governance Artifacts Enforced:**")
        st.code(st.session_state.context_layer.json(indent=2), language="json")

    # Render Proactive Alert
    st.info(f"The system has drafted the following proactive response tailored to your specific role.")
    with st.container(border=True):
        st.markdown(st.session_state.auto_intelligence_generated)

    st.divider()

    # --- HUMAN-IN-THE-LOOP CHAT ---
    st.markdown("### 💬 Human-in-the-Loop Refinement")
    st.caption("Chat with the OS to refine parameters, adjust tone, or approve the drafted strategy.")
    
    # Display History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])
            
    # Chat Input
    if prompt := st.chat_input("E.g., 'Make the tone more aggressive' or 'Approve and deploy to dashboard'"):
        # Append User Input
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): 
            st.markdown(prompt)
            
        # Get AI Response
        with st.chat_message("assistant"):
            with st.spinner("Refining operational parameters..."):
                response = query_groq(
                    prompt=prompt, 
                    system_context=st.session_state.auto_intelligence_generated, 
                    client=client
                )
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
else:
    st.markdown("### Welcome to the Sense & Respond OS")
    st.write("👈 Configure your industry parameters on the left and click **Run Sense & Respond Sequence** to detect anomalies and trigger an autonomous agent.")
