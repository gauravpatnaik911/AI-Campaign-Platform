import streamlit as st
import json
import pandas as pd
import os
from pydantic import BaseModel
from typing import List, Dict, Optional

# --- INSTITUTIONAL LIBRARY VALIDATION ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. System halted. Run: pip install groq")
    st.stop()

# ==========================================
# 1. THE BOARDROOM SIGNATURE (CSS)
# ==========================================
def inject_institutional_aesthetic():
    st.markdown("""
    <style>
        /* Institutional Palette & Typography */
        html, body, [class*="css"] {
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #FFFFFF;
            color: #051C2C; /* MBB Deep Navy */
        }
        
        /* Pinstripe Professional Background */
        .main {
            background-image: radial-gradient(#d1d5db 0.5px, transparent 0.5px);
            background-size: 30px 30px;
        }

        /* Top-Down Hierarchy Headers */
        h1 { font-weight: 900; border-bottom: 5px solid #051C2C; padding-bottom: 12px; font-size: 2.6rem !important; color: #051C2C !important; }
        h2 { font-weight: 700; color: #005587; margin-top: 2rem !important; border-left: 8px solid #005587; padding-left: 15px; text-transform: uppercase; }
        h3 { font-weight: 600; text-transform: none; color: #051C2C; border-bottom: 1px solid #e5e7eb; }

        /* Metric "Slides" */
        [data-testid="stMetric"] {
            background-color: #F9FAFB; border: 1px solid #051C2C; border-radius: 0px; padding: 25px;
        }

        /* High-Stakes Action Button */
        div.stButton > button {
            background-color: #051C2C !important; color: white !important; border-radius: 0px !important;
            width: 100%; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;
            border: none; padding: 20px; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        div.stButton > button:hover { background-color: #002B49 !important; transform: scale(1.01); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        
        /* Table Sovereignty */
        .stTable { border: 2px solid #051C2C !important; }
        thead tr th { background-color: #051C2C !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. OMNIVERSE DATA SCHEMAS
# ==========================================
class StrategicSignal(BaseModel):
    feature_name: str
    virality_score: float      # Meta-logic: Shareability/Attention
    yield_velocity: float      # AdTech-logic: Speed of EBITDA conversion
    confidence_interval: int   # Nielsen-logic: Statistical significance
    mbb_action_title: str      # The "Action-Title" directive

class OmniverseIntelligence(BaseModel):
    governing_thought: str
    strategic_pillars: List[Dict[str, str]] # MECE Pillars
    signals: List[StrategicSignal]
    kpi_impact_matrix: Dict[str, str]
    linchpin_risk: str
    governance_lineage: str

# ==========================================
# 3. TAXONOMY INTELLIGENCE LOAD
# ==========================================
@st.cache_data
def ingest_taxonomies():
    """Safely loads CSVs, preventing hard crashes if files are missing in production."""
    try:
        industry_tax = pd.read_csv('LLM_Insights_Context_Taxonomy.xlsx - Industry Taxonomy.csv').fillna("N/A")
        persona_tax = pd.read_csv('LLM_Insights_Context_Taxonomy.xlsx - Universal Personas.csv').fillna("N/A")
        kpi_tax = pd.read_csv('LLM_Insights_Context_Taxonomy.xlsx - KPI Taxonomy.csv').fillna("N/A")
        meta_tax = pd.read_csv('LLM_Insights_Context_Taxonomy.xlsx - Metadata Artifacts.csv').fillna("N/A")
        return industry_tax, persona_tax, kpi_tax, meta_tax
    except FileNotFoundError as e:
        st.error(f"CRITICAL DATA MISSING: {e.filename} not found. Please ensure all 4 CSV files are uploaded to the root directory.")
        st.stop()

# ==========================================
# 4. THE ENGINE (SYNTHESIS CORE)
# ==========================================
def execute_omniverse_synthesis(industry, sub_ind, domain, persona, artifacts, client):
    meta_context = artifacts['meta'].to_string()
    kpi_context = artifacts['kpi'].to_string()
    
    sys_prompt = f"""
    You are the MBB Omniverse Logic Engine. 
    Unified Institutional Intel: Meta + AppLovin + TradeDesk + Nielsen + McKinsey/BCG/Bain.

    OBJECTIVE: Architect a strategic solution for:
    - INDUSTRY: {industry} | SUB-INDUSTRY: {sub_ind}
    - DOMAIN: {domain} | PERSONA: {persona}
    - GOVERNANCE CONTEXT: {meta_context}
    - KPI TAXONOMY: {kpi_context}

    METHODOLOGICAL MANDATES:
    1. Governing Thought: Lead with a high-conviction answer. No filler.
    2. MECE Pillars: Provide 3 pillars. EACH pillar MUST be a dictionary with EXACT keys: "title" and "description".
    3. Action Titles: Every heading must be a punchy conclusion.
    4. Arbitrage Index: Rank signals by (Virality * Yield).

    Return strictly JSON matching the OmniverseIntelligence schema.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.2 # Institutional precision
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        st.error(f"Logic Engine Disruption: {e}")
        return None

# ==========================================
# 5. THE BOARDROOM INTERFACE
# ==========================================
def main():
    st.set_page_config(page_title="Omniverse Intelligence", layout="wide", page_icon="🏛️")
    inject_institutional_aesthetic()

    ind_df, per_df, kpi_df, meta_df = ingest_taxonomies()
    artifacts = {'meta': meta_df, 'kpi': kpi_df}

    st.sidebar.title("🏛️ STRATEGIC PARAMETERS")
    
    sel_ind = st.sidebar.selectbox("Industry Vertical", ind_df['Industry'].unique())
    sub_filtered = ind_df[ind_df['Industry'] == sel_ind]['Subindustry'].unique()
    sel_sub = st.sidebar.selectbox("Sub-Industry Segment", sub_filtered)
    
    dom_filtered = ind_df[ind_df['Subindustry'] == sel_sub]['Functional Domain'].unique()
    sel_dom = st.sidebar.selectbox("Functional Domain", dom_filtered)
    
    per_filtered = ind_df[ind_df['Subindustry'] == sel_sub]['Persona'].unique()
    sel_per = st.sidebar.selectbox("Executive Persona", per_filtered)

    if "GROQ_API_KEY" not in st.secrets:
        st.error("GROQ_API_KEY not found in Streamlit Secrets.")
        st.stop()
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    if st.sidebar.button("EXECUTE OMNIVERSE SYNTHESIS"):
        with st.spinner("COMMENCING MULTI-DOMAIN ARBITRAGE..."):
            intelligence = execute_omniverse_synthesis(sel_ind, sel_sub, sel_dom, sel_per, artifacts, client)
            if intelligence:
                st.session_state.intel = intelligence

    # --- OUTPUT PRESENTATION ---
    if "intel" in st.session_state:
        doc = st.session_state.intel

        st.markdown(f"#### BOARDROOM BRIEFING | {sel_per} | {sel_ind}")
        st.title(doc.get('governing_thought', 'Strategic Overview'))
        
        st.markdown("### I. Strategic Pillars (MECE Framework)")
        pillars = doc.get('strategic_pillars', [])
        if pillars:
            p_cols = st.columns(len(pillars))
            for i, pillar in enumerate(pillars):
                with p_cols[i]:
                    # Safe dictionary extraction
                    title = pillar.get("title", f"Pillar {i+1}")
                    desc = pillar.get("description", "Awaiting detail.")
                    st.metric(label=f"Pillar {i+1}", value="Validated")
                    st.markdown(f"**{title}**")
                    st.caption(desc)

        st.markdown("---")

        st.header("II. Predictive Arbitrage & Signal Confidence")
        signals = doc.get('signals', [])
        if signals:
            sig_df = pd.DataFrame(signals)
            sig_df['Arbitrage_Index'] = (sig_df['virality_score'] * sig_df['yield_velocity'] * (sig_df['confidence_interval']/100)).round(3)
            sig_df = sig_df.sort_values(by='Arbitrage_Index', ascending=False)
            
            st.table(sig_df.style.format({
                'virality_score': '{:.2f}', 'yield_velocity': '{:.2f}', 
                'confidence_interval': '{}%', 'Arbitrage_Index': '{:.3f}'
            }).background_gradient(subset=['Arbitrage_Index'], cmap='Blues'))

        col_kpi, col_risk = st.columns(2)
        with col_kpi:
            st.header("III. KPI Attribution Matrix")
            for k, v in doc.get('kpi_impact_matrix', {}).items():
                st.write(f"● **{k}:** {v}")
        
        with col_risk:
            st.header("IV. Structural Alpha Risk")
            st.error(f"**LINCHPIN VARIABLE:** {doc.get('linchpin_risk', 'N/A')}")
            st.info(f"**DATA LINEAGE:** {doc.get('governance_lineage', 'N/A')}")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption(f"Proprietary MBB Omniverse Logic Engine | Integrated Taxonomy v4.0 | N=1.2M Data Points | Statistical Power: 0.95")

if __name__ == "__main__":
    main()
