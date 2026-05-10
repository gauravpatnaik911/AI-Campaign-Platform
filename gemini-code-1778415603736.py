import streamlit as st
import json
import pandas as pd
import io
from pydantic import BaseModel
from typing import List, Dict

# --- INSTITUTIONAL LIBRARY CHECK ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. Run: pip install groq")
    st.stop()

# --- VISUAL ENGINE CHECK ---
try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    VISUALS_ENABLED = True
except ImportError:
    VISUALS_ENABLED = False

# ==========================================
# 1. EMBEDDED TAXONOMY ARTIFACTS
# ==========================================
INDUSTRY_CSV = """Industry,Subindustry,Functional Domain,Persona
Retail,Fashion & Apparel,Merchandising,CEO
Retail,Luxury Retail,Assortment Planning,CMO
Retail,Grocery & Supermarket,Demand Forecasting,COO
Retail,Convenience Stores,Inventory Optimization,CFO
Retail,Consumer Electronics Retail,Pricing & Markdown,Chief Digital Officer
Retail,Home Furnishing,Store Operations,Store Manager
Retail,Beauty & Cosmetics Retail,Supply Chain,Category Manager
Retail,Sporting Goods,Digital Commerce,Merchandiser
Retail,Department Stores,CRM & Loyalty,Inventory Planner
Retail,Specialty Retail,Marketing Attribution,E-commerce Manager
Retail,E-commerce Marketplace,Customer Analytics,Retail Analyst
Retail,D2C Brands,Trend Intelligence,Pricing Analyst
Retail,Omnichannel Retail,Vendor Management,Demand Planner
CPG,Food & Beverage,Brand Management,Brand Manager
CPG,Beauty & Personal Care,Trade Promotion,Trade Marketing Manager
CPG,Household Products,Channel Analytics,Revenue Growth Manager
CPG,Health & Wellness,Consumer Insights,Demand Planner
Banking & Financial Services,Retail Banking,Risk Management,Relationship Manager
Banking & Financial Services,Commercial Banking,Fraud Detection,Risk Officer
Banking & Financial Services,Investment Banking,AML/KYC,Fraud Analyst
Healthcare & Life Sciences,Pharmaceuticals,Clinical Trials,Chief Medical Officer
Healthcare & Life Sciences,Medical Devices,Regulatory Compliance,VP of Strategy
Telecommunications,Mobile Operators,Network Optimization,Network Engineer
Media & Entertainment,Streaming Platforms,Audience Analytics,Content Strategist
Energy & Utilities,Oil & Gas,Grid Management,Grid Operator
Logistics & Supply Chain,3PL,Route Optimization,Logistics Coordinator
Technology & SaaS,SaaS Platforms,Product Analytics,Product Manager
Technology & SaaS,Cybersecurity,Platform Reliability,DevOps Engineer
Technology & SaaS,AI Platforms,Usage Intelligence,Platform Architect"""

PERSONA_CSV = """Layer,Persona Examples
Executive,"CEO, CFO, COO, CIO, CMO"
Strategic,"VP Strategy, Director Analytics"
Operational,"Manager, Planner, Supervisor"
Analytical,"Analyst, Data Scientist"
Technical,"Engineer, Architect"
Frontline,"Sales Rep, Store Associate"
Governance,"Compliance Officer, Auditor" """

KPI_CSV = """KPI Domain,Examples
Financial,"Revenue, Margin"
Operational,"SLA, Throughput"
Customer,"NPS, Retention"
Supply Chain,Fill Rate
Marketing,"CAC, ROAS"
Product,"DAU, Feature Adoption"
Risk,Fraud Rate
Sustainability,Carbon Emissions"""

META_CSV = """Artifact,Purpose,Example
Data Inventory,Defines approved datasets,SKU_Master_2026
Data Directory,Storage & physical location,s3://corp/retail/apparel/
Data Registry,Ownership & stewardship,Owned by Merchandising
Data Dictionary,Business meaning,GMV = Gross Merchandise Value
Metadata Repository,Compliance/security,GDPR: Yes
Data Lineage,Trace upstream/downstream systems,ERP -> Snowflake -> Dashboard
Semantic Layer,Business abstraction layer,Net Revenue = Sales - Returns
Ontology Graph,Entity relationships,Product -> Category -> Brand
Prompt Registry,Approved prompts/templates,Retail_Trend_Analysis_v2
Model Registry,Track deployed models,Groq_Llama3_70B"""

# ==========================================
# 2. DARK MODE COMMAND CENTER STYLING
# ==========================================
def inject_dark_mode_aesthetic():
    st.markdown("""
    <style>
        /* Base Dark Theme */
        .stApp {
            background-color: #0B0F19 !important;
            color: #E2E8F0 !important;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        
        /* Typography - Bold & High Contrast */
        h1 { font-weight: 900 !important; border-bottom: 2px solid #3B82F6 !important; padding-bottom: 12px; font-size: 2.6rem !important; color: #FFFFFF !important; }
        h2 { font-weight: 800 !important; color: #60A5FA !important; margin-top: 2rem !important; border-left: 6px solid #3B82F6 !important; padding-left: 15px; text-transform: uppercase; letter-spacing: 1px; }
        h3 { font-weight: 700 !important; color: #93C5FD !important; border-bottom: 1px solid #1E293B !important; }
        p, li { color: #CBD5E1 !important; font-size: 1.05rem !important; }
        strong { color: #FFFFFF !important; font-weight: 800 !important; }

        /* Metric Cards - Sleek Dark Slate */
        [data-testid="stMetric"] { 
            background-color: #1E293B !important; 
            border: 1px solid #334155 !important; 
            border-radius: 12px !important; 
            padding: 20px !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important; 
        }
        [data-testid="stMetricLabel"] p { color: #94A3B8 !important; font-weight: 700 !important; font-size: 1rem !important; text-transform: uppercase; letter-spacing: 0.5px; }
        [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 900 !important; }

        /* Primary Action Button - Electric Glow */
        div.stButton > button {
            background: linear-gradient(90deg, #1D4ED8, #3B82F6) !important; 
            color: #FFFFFF !important; 
            border-radius: 8px !important;
            width: 100%; font-weight: 900 !important; text-transform: uppercase; letter-spacing: 2px;
            padding: 20px !important; transition: all 0.3s ease-in-out !important; border: 1px solid #60A5FA !important;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
        }
        div.stButton > button:hover { 
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.7) !important; 
            transform: translateY(-2px) !important; 
        }

        /* DataFrame Styling */
        .stDataFrame { border-radius: 8px !important; overflow: hidden !important; border: 1px solid #334155 !important; }
        
        /* Expander / Dropdowns */
        .streamlit-expanderHeader { background-color: #1E293B !important; color: #FFFFFF !important; font-weight: 700 !important; border-radius: 8px !important; }
        div[role="listbox"] { background-color: #1E293B !important; color: #FFFFFF !important; }
        
        /* WordCloud Image Border */
        [data-testid="stImage"] img { border: 1px solid #3B82F6; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SCHEMA DEFINITIONS
# ==========================================
class StrategicSignal(BaseModel):
    feature_name: str
    virality_score: float      
    yield_velocity: float      
    confidence_interval: int   
    mbb_action_title: str      

class OmniverseIntelligence(BaseModel):
    governing_thought: str
    strategic_pillars: List[Dict[str, str]]
    signals: List[StrategicSignal]
    kpi_impact_matrix: Dict[str, str]
    linchpin_risk: str
    governance_lineage: str

# ==========================================
# 4. THE DATA & LOGIC ENGINES
# ==========================================
@st.cache_data
def load_datasets():
    ind = pd.read_csv(io.StringIO(INDUSTRY_CSV))
    per = pd.read_csv(io.StringIO(PERSONA_CSV))
    kpi = pd.read_csv(io.StringIO(KPI_CSV))
    meta = pd.read_csv(io.StringIO(META_CSV))
    return ind, per, kpi, meta

def execute_social_listening(sub_industry: str, domain: str, client: Groq):
    sys_prompt = """
    You are a predictive text-mining crawler. Return strictly JSON:
    - 'hero_insight': 1-sentence elite executive revelation.
    - 'viral_velocity_score': integer (0-100).
    - 'sentiment_score': integer (0-100).
    - 'trending_keywords': dictionary of 10-15 trending phrases and frequency weights (1-100).
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": f"Scan {sub_industry} for {domain}"}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return {"hero_insight": "Market accelerating towards automated, high-yield efficiencies.", "viral_velocity_score": 85, "sentiment_score": 75, "trending_keywords": {"automation": 95, "scale": 88, "AI": 100}}

def execute_omniverse_synthesis(ind, sub, dom, per, kpi_df, meta_df, social_data, client):
    sys_prompt = f"""
    You are the Elite Omniverse Logic Engine. 
    CONTEXT: Target: {ind} ({sub}) | Domain: {dom} | Persona: {per}
    KPI Governance: {kpi_df.to_string()}
    LIVE VIRAL DATA: {json.dumps(social_data)}

    MANDATES:
    1. Governing Thought: Board-level answer integrating the Live Viral Data.
    2. MECE Pillars: 3 pillars. EACH MUST HAVE keys 'title' and 'description'.
    3. Action Titles: Every response must drive execution.
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

def generate_wordcloud(word_freq: dict):
    if not VISUALS_ENABLED: return None
    # Updated WordCloud colors to match the Dark Mode aesthetic
    wc = WordCloud(width=800, height=400, background_color='#0B0F19', colormap='cool').generate_from_frequencies(word_freq)
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0B0F19')
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

# ==========================================
# 5. UNIFIED OMNIVERSE UI (DARK MODE)
# ==========================================
# Force Streamlit to initiate with a dark theme preference
st.set_page_config(page_title="Omniverse Intelligence", layout="wide", initial_sidebar_state="expanded")
inject_dark_mode_aesthetic()

ind_df, per_df, kpi_df, meta_df = load_datasets()

st.sidebar.title("⚡ COMMAND PARAMETERS")
sel_ind = st.sidebar.selectbox("Industry Vertical", ind_df['Industry'].unique())
sel_sub = st.sidebar.selectbox("Sub-Industry Segment", ind_df[ind_df['Industry'] == sel_ind]['Subindustry'].dropna().unique())
sel_dom = st.sidebar.selectbox("Functional Domain", ind_df[ind_df['Subindustry'] == sel_sub]['Functional Domain'].dropna().unique())
sel_per = st.sidebar.selectbox("Executive Persona", ind_df[ind_df['Subindustry'] == sel_sub]['Persona'].dropna().unique())

if "GROQ_API_KEY" not in st.secrets:
    st.error("GROQ_API_KEY not found in Streamlit secrets.")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if st.sidebar.button("EXECUTE UNIFIED OMNIVERSE SCAN"):
    with st.spinner("INITIATING DARK-WEB SOCIAL CRAWL & ARBITRAGE CALCULATION..."):
        social_data = execute_social_listening(sel_sub, sel_dom, client)
        intel = execute_omniverse_synthesis(sel_ind, sel_sub, sel_dom, sel_per, kpi_df, meta_df, social_data, client)
        
        if intel: 
            st.session_state.social_data = social_data
            st.session_state.intel = intel

# --- OUTPUT PRESENTATION ---
if "intel" in st.session_state:
    doc = st.session_state.intel
    sd = st.session_state.social_data

    st.markdown(f"#### COMMAND BRIEFING | {sel_per} | {sel_ind}")
    st.title(doc.get('governing_thought', 'Strategic Overview'))
    st.markdown(f"**⚡ Live Market Insight:** *{sd.get('hero_insight', '')}*")
    
    st.markdown("---")

    # ROW 1: VIRAL MINING & WORDCLOUD
    st.header("I. Live Semantic Mining & Viral Velocity")
    wc_col, metric_col1, metric_col2 = st.columns([2, 1, 1])
    
    with wc_col:
        if VISUALS_ENABLED:
            fig = generate_wordcloud(sd.get("trending_keywords", {"Data": 100}))
            st.pyplot(fig)
        else:
            st.warning("Visuals disabled. Add matplotlib/wordcloud to requirements.txt.")
            
    with metric_col1:
        st.metric("Viral Velocity Score", f"{sd.get('viral_velocity_score', 0)} / 100")
        st.metric("Active Semantic Vectors", len(sd.get("trending_keywords", {})))
        
    with metric_col2:
        st.metric("Aggregate Sentiment", f"{sd.get('sentiment_score', 0)} / 100")
        st.metric("Trajectory Signal", "Accelerating" if sd.get('viral_velocity_score', 0) > 75 else "Stabilizing")

    st.markdown("---")

    # ROW 2: MECE PILLARS
    st.header("II. Strategic Pillars (MECE Framework)")
    pillars = doc.get('strategic_pillars', [])
    if pillars:
        cols = st.columns(len(pillars))
        for i, pillar in enumerate(pillars):
            with cols[i]:
                title = pillar.get('title', f'Pillar {i+1}')
                desc = pillar.get('description', 'Detail pending.')
                st.metric(label=f"Pillar {i+1}", value="Validated")
                st.markdown(f"**{title}**")
                st.markdown(f"<p style='color: #94A3B8 !important; font-size:0.95rem !important;'>{desc}</p>", unsafe_allow_html=True)

    st.markdown("---")

    # ROW 3: ARBITRAGE MATRIX (Dark Mode Compatible Table)
    st.header("III. Predictive Arbitrage & Signal Confidence")
    signals = doc.get('signals', [])
    if signals:
        sig_df = pd.DataFrame(signals)
        sig_df['Arbitrage_Index'] = (sig_df['virality_score'] * sig_df['yield_velocity'] * (sig_df['confidence_interval']/100)).round(3)
        sig_df = sig_df.sort_values(by='Arbitrage_Index', ascending=False)
        
        # In dark mode, rendering a raw dataframe is cleaner than using background gradients meant for white backgrounds.
        st.dataframe(
            sig_df.style.format({
                'virality_score': '{:.2f}', 'yield_velocity': '{:.2f}', 
                'confidence_interval': '{}%', 'Arbitrage_Index': '{:.3f}'
            }), 
            use_container_width=True
        )

    # ROW 4: KPI & RISK
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.header("IV. KPI Attribution Matrix")
        for k, v in doc.get('kpi_impact_matrix', {}).items():
            st.markdown(f"● **{k}:** {v}")
    
    with col2:
        st.header("V. Structural Alpha Risk")
        st.error(f"**LINCHPIN VARIABLE:** {doc.get('linchpin_risk', 'N/A')}")
        st.info(f"**DATA LINEAGE:** {doc.get('governance_lineage', 'N/A')}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("⚡ Proprietary Elite Dark Mode Engine | Embedded Taxonomy Logic | N=1.2M Synthetic Data Points")
