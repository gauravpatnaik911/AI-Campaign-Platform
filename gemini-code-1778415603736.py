import streamlit as st
from groq import Groq
import json
from pydantic import BaseModel
from typing import List, Dict, Optional

# --- 1. DATA ARCHITECTURE (Governance Artifacts) ---
class ContextLayer(BaseModel):
    inventory: str
    directory: str
    registry: str
    dictionary: Dict[str, str]
    metadata_repo: str

# --- 2. GOVERNANCE & DOCUMENTATION ENGINE ---
def get_metadata_context(industry: str, sub_ind: str, persona: str) -> ContextLayer:
    """Provides the absolute governance guardrails for the LLM."""
    # Documentation definitions as requested
    inventories = {
        "Fashion & Apparel": "SKU_Master_2026, Social_Crawl_V4, Fabric_Sustainability_Index",
        "Consumer Electronics": "Hardware_Spec_Repo, Tech_Sentiment_V2, Return_Log_Analytics",
        "Food & Beverage": "Supply_Chain_ERP, Consumer_Health_Panel_2026, Freshness_Logs",
        "Personal Care & Beauty": "Ingredient_Safety_DB, IG_Beauty_Trends, Shelf_Velocity_Data"
    }
    
    dictionaries = {
        "Fashion & Apparel": {"Trend_Velocity": "Mentions/Day on TikTok", "Sell-Through": "Actual vs Projected Sales %"},
        "Food & Beverage": {"LTV": "Customer Lifetime Value (12mo)", "Waste_Index": "Unsold perishable delta"}
    }

    return ContextLayer(
        inventory=inventories.get(sub_ind, "Enterprise_Data_Lake_General"),
        directory=f"s3://corp-data/{industry.lower()}/{sub_ind.lower().replace(' ', '_')}/",
        registry=f"Verified by {persona}_Dept | Version 2026.Q2",
        dictionary=dictionaries.get(sub_ind, {"KPI": "Key Performance Indicator"}),
        metadata_repo=f"Compliance: GDPR/SOC2 | Tags: {sub_ind}, {persona}, Strategic_Plan_2026"
    )

# --- 3. LOGIC ENGINES ---
def simulate_external_scrape(sub_industry: str, client: Groq):
    """Synthetic Scraper using Groq JSON mode."""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Return JSON with keys: 'video_trends' (list) and 'web_sentiment' (string)."},
                {"role": "user", "content": f"Extract 2026 market signals for {sub_industry}"}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except:
        return {"video_trends": ["Sustainability", "AI Personalization"], "web_sentiment": "Positive"}

# --- 4. STREAMLIT UI ---
st.set_page_config(page_title="Enterprise AI Insights", layout="wide")

# API Key Validation
if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ_API_KEY in Secrets. Please add it to continue.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Sidebar Context Selection
st.sidebar.title("🛠️ Context Engine")
industry = st.sidebar.selectbox("Industry", ["Retail", "CPG"])
sub_options = {
    "Retail": ["Fashion & Apparel", "Consumer Electronics", "Home & Furniture"],
    "CPG": ["Food & Beverage", "Personal Care & Beauty", "Household Cleaning"]
}
sub_ind = st.sidebar.selectbox("Sub-Industry", sub_options[industry])
persona = st.sidebar.selectbox("Persona", ["Designer", "Campaign Analyst", "Merchandiser", "Brand Manager", "Digital Marketer"])

# State Management
if "intel" not in st.session_state: st.session_state.intel = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []

if st.sidebar.button("Generate Intelligence", type="primary"):
    with st.spinner("Analyzing Governance Artifacts..."):
        context = get_metadata_context(industry, sub_ind, persona)
        scrape = simulate_external_scrape(sub_ind, client)
        
        sys_prompt = f"""
        You are an elite {persona} working in {sub_ind}.
        GUARDRAILS: {context.json()}
        EXTERNAL DATA: {scrape}
        
        TASK: Generate a high-priority intelligence report. 
        - IF Designer: Generate 3 detailed prompts for moodboard sketches.
        - IF Analyst: Generate Target ROAS/CPA metrics.
        - GENERAL: Use professional, data-driven tone. No conversational filler.
        """
        
        try:
            resp = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.session_state.intel = resp
            st.session_state.context_doc = context
        except Exception as e:
            st.error(f"API Error: {e}")

# --- 5. RESULTS DISPLAY ---
if st.session_state.intel:
    st.header(f"Strategic Briefing: {persona}")
    
    # Metadata Documentation Module
    with st.expander("📚 Metadata Governance Documentation"):
        doc = st.session_state.context_doc
        c1, c2 = st.columns(2)
        c1.markdown(f"**Data Inventory:** `{doc.inventory}`")
        c1.markdown(f"**Data Directory:** `{doc.directory}`")
        c2.markdown(f"**Data Registry:** `{doc.registry}`")
        c2.markdown(f"**Metadata Repository:** `{doc.metadata_repo}`")
        st.info(f"**Data Dictionary:** {doc.dictionary}")

    st.markdown("---")

    # Persona-Specific Visual Logic
    if persona == "Designer":
        st.subheader("🎨 AI-Generated Design Sketches")
        # Fixed blank image issue with dynamic keyword search
        search_term = sub_ind.lower().replace(" ", "-")
        cols = st.columns(3)
        for i in range(3):
            img_url = f"https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&q=80&w=400&q={i}" if "Fashion" in sub_ind else f"https://loremflickr.com/400/400/{search_term},sketch?lock={i}"
            cols[i].image(img_url, caption=f"Design Sketch Proposal {i+1}")

    elif persona == "Campaign Analyst":
        st.subheader("📊 Performance Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Recommended ROAS", "4.8x", "+0.4")
        col2.metric("Projected CPA", "$9.50", "-12%")
        col3.metric("Engagement Goal", "5.2%", "+1.8%")

    st.markdown(st.session_state.intel)

    # 6. FOLLOW-UP CHAT
    st.markdown("---")
    st.subheader("💬 Refinement Chat")
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if prompt := st.chat_input("Adjust strategy..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            full_msg = f"Base Context: {st.session_state.intel}\nUser Query: {prompt}"
            r = client.chat.completions.create(
                messages=[{"role": "user", "content": full_msg}],
                model="llama-3.1-8b-instant"
            ).choices[0].message.content
            st.markdown(r)
            st.session_state.chat_history.append({"role": "assistant", "content": r})
