%%writefile app.py
import streamlit as st
from groq import Groq
import json
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- 1. DATA ARCHITECTURE (Pydantic Models) ---
class DataInventory(BaseModel):
    source_names: List[str]
    update_frequency: str

class DataDirectory(BaseModel):
    location_path: str
    access_level: str

class DataRegistry(BaseModel):
    owner: str
    version: str

class DataDictionary(BaseModel):
    terms: Dict[str, str]

class MetadataRepository(BaseModel):
    tags: List[str]
    compliance_status: str

class ContextLayer(BaseModel):
    inventory: DataInventory
    directory: DataDirectory
    registry: DataRegistry
    dictionary: DataDictionary
    metadata: MetadataRepository

# --- 2. LOGIC ENGINES ---
def get_governance_context(sub_industry: str, persona: str) -> ContextLayer:
    """Mock Seeding: Dynamic Contextual Guardrails"""
    return ContextLayer(
        inventory=DataInventory(source_names=[f"{sub_industry}_Insight_Stream", "Global_Market_Pulse"], update_frequency="Real-time"),
        directory=DataDirectory(location_path=f"s3://ent-data-lake/{sub_industry.lower().replace(' ', '_')}/", access_level="Enterprise_Admin"),
        registry=DataRegistry(owner=f"{persona}_Department", version="2026.Q2.v1"),
        dictionary=DataDictionary(terms={"Engagement": "Total Interactions / Reach", "LTV": "Life Time Value"}),
        metadata=MetadataRepository(tags=[sub_industry, persona, "Strategic_Intelligence"], compliance_status="SOC2_Type_II")
    )

def simulate_external_scrape(sub_industry: str, client: Groq):
    """Synthetic Scraping Engine using Groq JSON mode."""
    prompt = f"Act as a web scraper. Generate real-time market trends for {sub_industry} in May 2026. Return ONLY JSON."
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Return JSON with keys: 'video_trends' (list) and 'web_sentiment' (string)."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return {"video_trends": ["Sustainability focus", "AI-driven personalization"], "web_sentiment": "High consumer optimism"}

# --- 3. STREAMLIT UI ---
st.set_page_config(page_title="Enterprise AI Insights", layout="wide")

# Sidebar for Setup
st.sidebar.title("🔑 Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

if not api_key:
    st.info("Please enter your Groq API key in the sidebar to begin.")
    st.stop()

client = Groq(api_key=api_key)

# Sidebar for Inputs
st.sidebar.title("🎯 Context Engine")
industry = st.sidebar.selectbox("Industry", ["Retail", "CPG"])
sub_options = {
    "Retail": ["Fashion & Apparel", "Consumer Electronics", "Home & Furniture"],
    "CPG": ["Food & Beverage", "Personal Care & Beauty", "Household Cleaning"]
}
sub_ind = st.sidebar.selectbox("Sub-Industry", sub_options[industry])
persona = st.sidebar.selectbox("Persona", ["Designer", "Campaign Analyst", "Merchandiser", "Brand Manager", "Digital Marketer"])

# State Management
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "intel" not in st.session_state: st.session_state.intel = None
if "scrape" not in st.session_state: st.session_state.scrape = None

if st.sidebar.button("Generate Intelligence", type="primary"):
    with st.spinner("Processing Context Layers..."):
        context = get_governance_context(sub_ind, persona)
        scrape_data = simulate_external_scrape(sub_ind, client)
        
        # System Prompt Orchestration
        sys_prompt = f"""
        Role: Elite {persona} in {sub_ind}.
        Context Guardrails: {context.json()}
        Simulated Scrape: {scrape_data}
        Task: Provide immediate, high-value strategic output.
        Constraint: No preamble. Use markdown.
        """
        
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama3-70b-8192"
        ).choices[0].message.content
        
        st.session_state.intel = response
        st.session_state.scrape = scrape_data

# Main Display
if st.session_state.intel:
    st.title(f"Strategic Intelligence: {persona}")
    
    with st.expander("🔍 Metadata Governance & Scrape Details"):
        st.json(st.session_state.scrape)
        
    st.markdown("---")
    
    # Persona UI Logic
    if persona == "Campaign Analyst":
        c1, c2, c3 = st.columns(3)
        c1.metric("Recommended ROAS", "4.8x", "+0.4")
        c2.metric("Est. CPA", "$8.40", "-$1.20")
        c3.metric("Reach Potential", "2.4M", "+15%")
    
    elif persona == "Designer":
        st.info("Moodboard Generation Active")
        st.image("https://placehold.co/800x200?text=AI+Visual+Prompt+Engine+Active")

    st.markdown(st.session_state.intel)
    
    # Chat Refinement
    st.markdown("---")
    st.subheader("💬 Strategy Refinement")
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
        
    if p := st.chat_input("Ask a follow-up..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            r = client.chat.completions.create(
                messages=[{"role": "system", "content": "Reference the previous intelligence to answer."},
                          {"role": "user", "content": p}],
                model="llama3-8b-8192"
            ).choices[0].message.content
            st.markdown(r)
            st.session_state.chat_history.append({"role": "assistant", "content": r})