import streamlit as st
from groq import Groq
import json
from pydantic import BaseModel
from typing import List, Dict

# --- 1. DATA ARCHITECTURE (Governance Artifacts) ---
class ContextLayer(BaseModel):
    data_inventory: str   # List of sources
    data_directory: str   # Storage paths/access
    data_registry: str    # Ownership & versioning
    data_dictionary: str  # Business terms definitions
    metadata_repo: str    # Compliance & tagging logic

# --- 2. GOVERNANCE METADATA ENGINE ---
def get_metadata_documentation(industry, sub_ind, persona):
    """Provides specific metadata documentation for the chosen context."""
    # This logic acts as the absolute guardrail for the LLM
    doc = {
        "Retail": {
            "Fashion & Apparel": {
                "inventory": "SKU_Master_v4, Trend_Crawl_2026, Social_Sentiment_API",
                "dictionary": {"Trend_Score": "0-100 score based on TikTok/IG velocity", "Sell-Through": "Actual vs Projected sales %"}
            }
        },
        "CPG": {
            "Food & Beverage": {
                "inventory": "Supply_Chain_Logistics_DB, Consumer_Health_Panel_2026",
                "dictionary": {"LTV": "Customer Lifetime Value based on 12-month reorder", "Shelf_Life_Index": "Days until expiration delta"}
            }
        }
    }
    
    # Generic Persona metadata for specific personas
    persona_metadata = {
        "Designer": "Compliance: Visual Brand Guidelines 2026. Data: RGB/CMYK Hex Mappings.",
        "Campaign Analyst": "Compliance: Privacy-First Attribution. Data: Conversion API (CAPI) Endpoints.",
        "Merchandiser": "Compliance: Inventory FIFO. Data: Warehouse Stock-to-Sales Ratios."
    }

    ind_data = doc.get(industry, {}).get(sub_ind, {"inventory": "Generic_Source", "dictionary": {}})
    
    return ContextLayer(
        data_inventory=ind_data["inventory"],
        data_directory=f"s3://{industry.lower()}-insights/{sub_ind.lower()}/",
        data_registry=f"Owner: {persona} | Version: 2026.5.10",
        data_dictionary=str(ind_data["dictionary"]),
        metadata_repo=persona_metadata.get(persona, "Standard Enterprise Compliance")
    )

# --- 3. CORE LOGIC ---
def simulate_external_scrape(sub_industry: str, client: Groq):
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Return JSON with keys: 'video_trends' (list) and 'web_sentiment' (string)."},
                {"role": "user", "content": f"2026 Market Trends for {sub_industry}"}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except:
        return {"video_trends": ["Sustainable Materials", "AI Customization"], "web_sentiment": "High Growth"}

# --- 4. UI COMPONENTS ---
st.set_page_config(page_title="AI Insight Platform v2", layout="wide")

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Add GROQ_API_KEY to Secrets.")
    st.stop()

# Sidebar
st.sidebar.header("Platform Controls")
industry = st.sidebar.selectbox("Industry", ["Retail", "CPG"])
sub_options = {"Retail": ["Fashion & Apparel", "Consumer Electronics"], "CPG": ["Food & Beverage", "Personal Care"]}
sub_ind = st.sidebar.selectbox("Sub-Industry", sub_options[industry])
persona = st.sidebar.selectbox("Persona", ["Designer", "Campaign Analyst", "Merchandiser", "Brand Manager", "Digital Marketer"])

if st.sidebar.button("Generate Intelligence", type="primary"):
    with st.spinner("Processing Data Artifacts..."):
        # Fetch Context & Scrape
        context_doc = get_metadata_documentation(industry, sub_ind, persona)
        scrape = simulate_external_scrape(sub_ind, client)
        
        # Build System Prompt with Guardrails
        sys_prompt = f"""
        Role: {persona} in {sub_ind}.
        GOVERNANCE METADATA: {context_doc.json()}
        LIVE SCRAPE: {scrape}
        TASK: Generate a high-level briefing. 
        IMPORTANT: If I am a Designer, provide 3 descriptive prompts for 'AI Visual Sketches'. 
        If I am an Analyst, provide target metrics (ROAS, CPA).
        """
        
        try:
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.session_state.intel = res
            st.session_state.context = context_doc
        except Exception as e:
            st.error(f"Error: {e}")

# --- 5. RESULTS DISPLAY ---
if "intel" in st.session_state:
    st.title(f"Intelligence Briefing: {persona}")
    
    # 1. METADATA DOCUMENTATION TAB
    with st.expander("📚 View Metadata & Governance Documentation"):
        c = st.session_state.context
        col1, col2 = st.columns(2)
        col1.write("**Data Inventory:**"); col1.code(c.data_inventory)
        col1.write("**Data Registry:**"); col1.code(c.data_registry)
        col2.write("**Data Dictionary:**"); col2.code(c.data_dictionary)
        col2.write("**Metadata Repository:**"); col2.code(c.metadata_repo)

    # 2. DESIGNER VISUALS
    if persona == "Designer":
        st.subheader("🎨 Visual Moodboard Sketches")
        cols = st.columns(3)
        for i in range(3):
            # Using a dynamic placeholder that simulates an AI generation result
            cols[i].image(f"https://placehold.co/400x400/222/white?text=Sketch+Idea+{i+1}", 
                          caption=f"AI Sketch Prompt {i+1}")
    
    # 3. ANALYST METRICS
    elif persona == "Campaign Analyst":
        st.subheader("📊 Key Performance Targets")
        c1, c2, c3 = st.columns(3)
        c1.metric("Optimal ROAS", "5.4x", "+0.2")
        c2.metric("Target CPA", "$9.50", "-12%")
        c3.metric("Engagement Goal", "4.8%", "+1.1%")

    st.markdown("---")
    st.markdown(st.session_state.intel)
