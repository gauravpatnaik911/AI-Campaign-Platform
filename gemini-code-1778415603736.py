import streamlit as st
from groq import Groq
import json
from pydantic import BaseModel
from typing import List, Dict

# --- 1. DATA ARCHITECTURE ---
class ContextLayer(BaseModel):
    inventory: Dict
    directory: Dict
    registry: Dict
    dictionary: Dict
    metadata: Dict

# --- 2. LOGIC ENGINES ---
def get_governance_context(sub_industry: str, persona: str) -> ContextLayer:
    """Provides the enterprise guardrails for the LLM."""
    return ContextLayer(
        inventory={"sources": [f"{sub_industry}_Internal", "Global_Market_Data"]},
        directory={"path": f"s3://enterprise/{sub_industry.lower()}/"},
        registry={"owner": persona, "status": "Verified"},
        dictionary={"KPI": "Key Performance Indicator", "CTR": "Click Through Rate"},
        metadata={"compliance": "GDPR/SOC2", "tags": [sub_industry, persona]}
    )

def simulate_external_scrape(sub_industry: str, client: Groq):
    """Synthetic Scraper using Groq JSON mode."""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Return JSON with keys: 'video_trends' (list) and 'web_sentiment' (string)."},
                {"role": "user", "content": f"Current 2026 trends for {sub_industry}"}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return {"video_trends": ["AI-Personalization", "Eco-Design"], "web_sentiment": "Positive"}

# --- 3. STREAMLIT UI SETUP ---
st.set_page_config(page_title="AI Insights Platform", layout="wide")

# Secure API Key Fetching
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# Sidebar UI
st.sidebar.title("Context Engine")
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

if st.sidebar.button("Generate Intelligence", type="primary"):
    with st.spinner("Analyzing Context Layers..."):
        context = get_governance_context(sub_ind, persona)
        scrape_data = simulate_external_scrape(sub_ind, client)
        
        sys_prompt = f"""
        Role: Elite {persona} in {sub_ind}.
        Context Guardrails: {context.json()}
        Simulated Scrape: {scrape_data}
        Task: Provide a strategic insight report for 2026. Use metrics for Analysts and Visual prompts for Designers.
        """
        
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.session_state.intel = response
        except Exception as e:
            st.error(f"Groq API Error: {str(e)}")

# --- 4. MAIN DISPLAY ---
if st.session_state.intel:
    st.title(f"2026 Strategic Intelligence: {persona}")
    st.markdown("---")
    
    # Persona-Specific Metrics
    if persona == "Campaign Analyst":
        c1, c2 = st.columns(2)
        c1.metric("Target ROAS", "5.2x", "+0.4")
        c2.metric("Target CPA", "$11.20", "-1.05")
    
    st.markdown(st.session_state.intel)
    
    # Chat Refinement
    st.markdown("---")
    st.subheader("💬 Strategy Chat")
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
        
    if p := st.chat_input("Ask a follow-up..."):
        st.session_state.chat_history.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            r = client.chat.completions.create(
                messages=[{"role": "user", "content": p}],
                model="llama-3.1-8b-instant"
            ).choices[0].message.content
            st.markdown(r)
            st.session_state.chat_history.append({"role": "assistant", "content": r})
