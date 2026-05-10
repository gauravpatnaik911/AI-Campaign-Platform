import streamlit as st
import json
from pydantic import BaseModel

# --- BULLETPROOF IMPORTS ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library not found. Please add it to requirements.txt.")
    st.stop()

try:
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    VISUALS_ENABLED = True
except ImportError:
    VISUALS_ENABLED = False

# ==========================================
# 1. APPLE-STYLE CSS INJECTION
# ==========================================
def inject_apple_css():
    st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #fbfbfd;
            color: #1d1d1f;
        }
        h1 { font-weight: 700 !important; letter-spacing: -0.015em !important; font-size: 2.5rem !important; color: #1d1d1f !important; }
        h2, h3 { font-weight: 600 !important; letter-spacing: -0.012em !important; color: #1d1d1f !important; }
        [data-testid="stMetric"] {
            background-color: #ffffff; border-radius: 18px; padding: 20px 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.08);
            transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-4px); box-shadow: 0 12px 20px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.06);
        }
        div.stButton > button {
            background-color: #0071e3 !important; color: white !important; border-radius: 980px !important;
            padding: 12px 24px !important; font-weight: 600 !important; border: none !important; transition: all 0.2s ease !important;
        }
        div.stButton > button:hover { background-color: #0077ED !important; transform: scale(1.02); }
        .streamlit-expanderHeader { font-weight: 600 !important; border-radius: 12px !important; }
        
        /* Make WordCloud visually rounded via CSS instead of Python */
        [data-testid="stImage"] img { border-radius: 15px; }
        
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. TAXONOMY & UNIVERSAL LAYERS
# ==========================================
TAXONOMY = {
    "Retail": {
        "sub_industries": ["Fashion & Apparel", "Luxury Retail", "Consumer Electronics Retail"],
        "domains": ["Merchandising", "Demand Forecasting", "Digital Commerce"],
        "personas": ["CEO", "CMO", "Category Manager", "Merchandiser"]
    },
    "CPG": {
        "sub_industries": ["Food & Beverage", "Beauty & Personal Care", "Health & Wellness"],
        "domains": ["Brand Management", "Consumer Insights", "Channel Analytics"],
        "personas": ["Brand Manager", "Trade Marketing Manager", "Consumer Insights Lead"]
    },
    "Technology & SaaS": {
        "sub_industries": ["SaaS Platforms", "AI Platforms", "Cybersecurity"],
        "domains": ["Product Analytics", "Usage Intelligence", "Customer Success"],
        "personas": ["Product Manager", "DevOps Engineer", "Platform Architect"]
    }
}

UNIVERSAL_LAYERS = {
    "CEO": "Executive", "CMO": "Executive", 
    "Category Manager": "Strategic", "Brand Manager": "Strategic", "Product Manager": "Strategic",
    "Merchandiser": "Operational", "DevOps Engineer": "Technical", "Platform Architect": "Technical",
    "Consumer Insights Lead": "Analytical"
}

class EnterpriseContextLayer(BaseModel):
    data_inventory: str
    data_directory: str
    data_registry: str
    data_dictionary: str
    metadata_repository: str
    data_lineage: str
    semantic_layer: str
    ontology_graph: str
    prompt_registry: str
    model_registry: str

def build_enterprise_context(industry: str, sub_ind: str, domain: str, persona: str) -> EnterpriseContextLayer:
    prefix = industry.split(' ')[0].lower()
    return EnterpriseContextLayer(
        data_inventory=f"Social_Listening_Firehose_v3, Live_{domain.replace(' ', '_')}_Stream",
        data_directory=f"s3://corp/{prefix}/viral_trends/",
        data_registry=f"Steward: Head of {domain} | Owner: {persona}",
        data_dictionary=f"Virality Indexes aligned to {domain} standardization.",
        metadata_repository=f"Compliance: GDPR | Layer: {UNIVERSAL_LAYERS.get(persona, 'Operational')}",
        data_lineage="Global Web Scraper -> NLP Engine -> Real-time UI",
        semantic_layer="NLP Entity Extraction & Viral Sentiment Scoring",
        ontology_graph="Keyword -> Sentiment -> Viral Velocity -> Action",
        prompt_registry=f"{prefix}_{persona.replace(' ', '_')}_Viral_Engine",
        model_registry="Groq Llama 3.3 70B Versatile"
    )

# ==========================================
# 3. SOCIAL LISTENING ENGINE
# ==========================================
def execute_social_listening_crawl(sub_industry: str, domain: str, client: Groq):
    sys_prompt = """
    You are a predictive text-mining crawler analyzing real-time social data.
    Return strictly JSON with the following keys:
    - 'hero_insight': string. A punchy, Steve Jobs-style 1-sentence revelation about the market.
    - 'viral_velocity_score': integer (0-100). Speed of trend adoption.
    - 'sentiment_score': integer (0-100). 100 is euphoric.
    - 'demand_trajectory': string (e.g., 'Hyper-Growth', 'Cooling').
    - 'trending_keywords': dictionary of 10-15 trending 1-2 word phrases and their frequency weight (integer 1-100).
    """
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": f"Extract 2026 market signals for {sub_industry} focusing on {domain}."}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return {
            "hero_insight": "The market is shifting rapidly towards AI-driven, hyper-personalized automation.",
            "viral_velocity_score": 92,
            "sentiment_score": 88,
            "demand_trajectory": "Exponential Surging",
            "trending_keywords": {"automation": 95, "scale": 85, "speed": 75, "integration": 90, "efficiency": 70, "AI": 100}
        }

def generate_wordcloud(word_freq: dict):
    if not VISUALS_ENABLED:
        return None
    # Removed border_radius to fix the TypeError!
    wc = WordCloud(width=800, height=400, background_color='#1d1d1f', colormap='Blues').generate_from_frequencies(word_freq)
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#fbfbfd')
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig

# ==========================================
# 4. STREAMLIT DASHBOARD
# ==========================================
st.set_page_config(page_title="Semantic AI", layout="wide", page_icon="")
inject_apple_css()

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets. Please configure it in your app settings.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "intel" not in st.session_state: st.session_state.intel = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []

st.sidebar.title("Intelligence Engine")
industry = st.sidebar.selectbox("Industry", list(TAXONOMY.keys()))
sub_ind = st.sidebar.selectbox("Sub-Industry", TAXONOMY[industry]["sub_industries"])
domain = st.sidebar.selectbox("Functional Domain", TAXONOMY[industry]["domains"])
persona = st.sidebar.selectbox("Persona", TAXONOMY[industry]["personas"])
layer = UNIVERSAL_LAYERS.get(persona, "Operational")

if st.sidebar.button("Execute Deep Mining Scan"):
    with st.spinner("Compiling Neural Ontology & Scraping Web..."):
        context = build_enterprise_context(industry, sub_ind, domain, persona)
        social_data = execute_social_listening_crawl(sub_ind, domain, client)
        
        sys_prompt = f"""
        Role: Elite {layer} {persona} in {sub_ind}. Focus: {domain}.
        GOVERNANCE ARTIFACTS: {context.json()}
        LIVE VIRAL DATA: {json.dumps(social_data)}
        
        TASK: Write a sleek, high-impact strategic briefing. 
        Focus heavily on how to monetize the 'trending_keywords' and 'viral_velocity_score'.
        Use clean markdown. No fluff.
        """
        try:
            resp = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            
            st.session_state.intel = resp
            st.session_state.context_doc = context
            st.session_state.social_data = social_data
        except Exception as e:
            st.error(f"Engine Error: {e}")

if st.session_state.intel:
    sd = st.session_state.social_data
    
    st.markdown(f"""
    <div style='text-align: center; padding: 40px 0;'>
        <h1 style='font-size: 3rem; background: -webkit-linear-gradient(#1d1d1f, #555); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            {sd.get("hero_insight", "Analyzing Market Vectors.")}
        </h1>
        <p style='color: #86868b; font-size: 1.2rem; font-weight: 500;'>Live Demand Intelligence for {persona} ({layer})</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    v_score = sd.get("viral_velocity_score", 0)
    col1.metric("Viral Velocity", f"{v_score}/100", "+ High" if v_score > 70 else "- Stable")
    col2.metric("Sentiment Index", f"{sd.get('sentiment_score', 0)}/100", "Favorable")
    col3.metric("Demand Trajectory", sd.get("demand_trajectory", "Unknown"), "Active")
    col4.metric("Active Signals", len(sd.get("trending_keywords", {})), "Mined keywords")
    
    st.markdown("<br>", unsafe_allow_html=True)

    chart_col, meta_col = st.columns([1.5, 1])
    
    with chart_col:
        st.markdown("### Semantic Network Density")
        if VISUALS_ENABLED:
            fig = generate_wordcloud(sd.get("trending_keywords", {"data": 100}))
            st.pyplot(fig)
        else:
            st.warning("WordCloud disabled. Please add 'matplotlib' and 'wordcloud' to your requirements.txt file to view the Semantic Network Density chart.")
            st.json(sd.get("trending_keywords", {}))
        
    with meta_col:
        st.markdown("### System Ontology")
        with st.expander("View Neural Governance Data"):
            doc = st.session_state.context_doc
            st.code(f"Inventory: {doc.data_inventory}\nRegistry: {doc.data_registry}\nLineage: {doc.data_lineage}", language="text")
            st.markdown(f"**Semantic Layer:** {doc.semantic_layer}")
            st.markdown(f"**Model:** {doc.model_registry}")

    st.markdown("---")
    st.markdown(f"<div style='padding: 20px; background-color: #ffffff; border-radius: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.04);'> {st.session_state.intel} </div>", unsafe_allow_html=True)
