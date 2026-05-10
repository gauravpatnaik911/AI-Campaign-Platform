import streamlit as st
from groq import Groq
import json
from pydantic import BaseModel
from typing import Dict, List

# ==========================================
# 1. TAXONOMY & MOCK DATABASE
# ==========================================
# Derived directly from your uploaded architecture CSVs
TAXONOMY = {
    "Retail": {
        "sub_industries": ["Fashion & Apparel", "Luxury Retail", "Grocery & Supermarket", "Consumer Electronics Retail", "E-commerce Marketplace"],
        "domains": ["Merchandising", "Assortment Planning", "Demand Forecasting", "Inventory Optimization", "Digital Commerce"],
        "personas": ["CEO", "CMO", "Category Manager", "Merchandiser", "Data Scientist", "Pricing Analyst"]
    },
    "CPG": {
        "sub_industries": ["Food & Beverage", "Beauty & Personal Care", "Household Products", "Health & Wellness"],
        "domains": ["Brand Management", "Trade Promotion", "Channel Analytics", "Consumer Insights"],
        "personas": ["Brand Manager", "Trade Marketing Manager", "Demand Planner", "Consumer Insights Lead"]
    },
    "Banking & Financial Services": {
        "sub_industries": ["Retail Banking", "Commercial Banking", "Investment Banking", "FinTech"],
        "domains": ["Risk Management", "Fraud Detection", "AML/KYC", "Portfolio Analytics"],
        "personas": ["Relationship Manager", "Risk Officer", "Fraud Analyst", "Investment Advisor"]
    },
    "Healthcare & Life Sciences": {
        "sub_industries": ["Hospitals & Providers", "Pharmaceuticals", "Medical Devices"],
        "domains": ["Patient Journey", "Clinical Operations", "Drug Discovery", "Clinical Trials"],
        "personas": ["Physician", "Hospital Administrator", "Clinical Analyst", "Medical Affairs Lead"]
    },
    "Technology & SaaS": {
        "sub_industries": ["SaaS Platforms", "Cloud Infrastructure", "Cybersecurity", "AI Platforms"],
        "domains": ["Product Analytics", "Customer Success", "Platform Reliability", "Usage Intelligence"],
        "personas": ["Product Manager", "Customer Success Manager", "DevOps Engineer", "Platform Architect"]
    }
}

UNIVERSAL_LAYERS = {
    "CEO": "Executive", "CMO": "Executive", 
    "Category Manager": "Strategic", "Brand Manager": "Strategic", "Product Manager": "Strategic",
    "Merchandiser": "Operational", "DevOps Engineer": "Technical", "Platform Architect": "Technical",
    "Data Scientist": "Analytical", "Fraud Analyst": "Analytical", "Pricing Analyst": "Analytical"
}

# ==========================================
# 2. DATA ARCHITECTURE (10 Metadata Artifacts)
# ==========================================
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
    """Dynamically builds the 10-layer governance context based on taxonomy selections."""
    prefix = industry.split(' ')[0].lower()
    
    return EnterpriseContextLayer(
        data_inventory=f"{sub_ind.replace(' ', '_')}_Master_DB, Live_{domain.replace(' ', '_')}_Stream",
        data_directory=f"s3://corp/{prefix}/{sub_ind.lower().replace(' ', '_')}/",
        data_registry=f"Steward: Head of {domain} | Owner: {persona}",
        data_dictionary=f"Domain KPIs aligned to {domain} standardization.",
        metadata_repository=f"Compliance: GDPR/CCPA | Security_Tier: High | Layer: {UNIVERSAL_LAYERS.get(persona, 'Operational')}",
        data_lineage=f"Snowflake Data Warehouse -> dbt Models -> {persona} Dashboards",
        semantic_layer=f"Business Logic Abstraction for {industry} Metrics",
        ontology_graph=f"Entity Relations: Customer -> Product -> {domain} -> Channel",
        prompt_registry=f"Approved Template: {prefix}_{persona.replace(' ', '_')}_v3",
        model_registry="Primary: Groq_Llama_3.3_70B_Versatile | Fallback: Llama_3.1_8B"
    )

# ==========================================
# 3. SYNTHETIC SCRAPING ENGINE
# ==========================================
def simulate_external_scrape(sub_industry: str, domain: str, client: Groq):
    """Synthetic Scraper using Groq JSON mode."""
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Return JSON with keys: 'market_signals' (list) and 'domain_sentiment' (string)."},
                {"role": "user", "content": f"Extract 2026 market signals for {sub_industry} focusing on {domain}."}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except:
        return {"market_signals": ["AI Integration", "Process Automation"], "domain_sentiment": "High Growth Potential"}

# ==========================================
# 4. STREAMLIT UI & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="Enterprise Semantic AI", layout="wide", page_icon="🧠")

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ_API_KEY in Secrets. Please add it to continue.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "intel" not in st.session_state: st.session_state.intel = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# --- Cascading Sidebar UI ---
st.sidebar.title("🧠 Semantic Engine")
st.sidebar.markdown("Configure Taxonomy Parameters")

industry = st.sidebar.selectbox("Industry", list(TAXONOMY.keys()))
sub_ind = st.sidebar.selectbox("Sub-Industry", TAXONOMY[industry]["sub_industries"])
domain = st.sidebar.selectbox("Functional Domain", TAXONOMY[industry]["domains"])
persona = st.sidebar.selectbox("Persona", TAXONOMY[industry]["personas"])

layer = UNIVERSAL_LAYERS.get(persona, "Operational")
st.sidebar.info(f"**Mapped Layer:** {layer}")

if st.sidebar.button("Generate Intelligence", type="primary"):
    with st.spinner("Compiling 10-Layer Ontology & Executing Models..."):
        context = build_enterprise_context(industry, sub_ind, domain, persona)
        scrape = simulate_external_scrape(sub_ind, domain, client)
        
        sys_prompt = f"""
        You are an elite AI operating at the {layer} level as a {persona} in the {sub_ind} sector.
        Your focus is {domain}.
        
        STRICT GOVERNANCE ARTIFACTS: {context.json()}
        EXTERNAL SCRAPE DATA: {scrape}
        
        TASK: Generate a highly professional, highly strategic intelligence briefing.
        - Emphasize the semantic relationships and ontology of the data.
        - If {layer} is Executive or Strategic, focus on Financial/Customer KPIs.
        - If {layer} is Technical or Analytical, focus on System architecture and granular metrics.
        - Format clearly using markdown. Do not use conversational filler.
        """
        
        try:
            resp = client.chat.completions.create(
                messages=[{"role": "system", "content": sys_prompt}],
                model="llama-3.3-70b-versatile"
            ).choices[0].message.content
            st.session_state.intel = resp
            st.session_state.context_doc = context
            st.session_state.scrape_doc = scrape
        except Exception as e:
            st.error(f"Groq API Error: {e}")

# ==========================================
# 5. MAIN DASHBOARD RENDER
# ==========================================
if st.session_state.intel:
    st.header(f"Strategic Briefing: {persona} ({layer})")
    
    # Render the 10 Metadata Artifacts
    with st.expander("🔐 View 10-Layer Semantic Metadata Architecture", expanded=False):
        doc = st.session_state.context_doc
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**1. Data Inventory:** `{doc.data_inventory}`")
            st.markdown(f"**2. Data Directory:** `{doc.data_directory}`")
            st.markdown(f"**3. Data Registry:** `{doc.data_registry}`")
        with col2:
            st.markdown(f"**4. Data Dictionary:** `{doc.data_dictionary}`")
            st.markdown(f"**5. Metadata Repository:** `{doc.metadata_repository}`")
            st.markdown(f"**6. Data Lineage:** `{doc.data_lineage}`")
        with col3:
            st.markdown(f"**7. Semantic Layer:** `{doc.semantic_layer}`")
            st.markdown(f"**8. Ontology Graph:** `{doc.ontology_graph}`")
            st.markdown(f"**9. Prompt Registry:** `{doc.prompt_registry}`")
            st.markdown(f"**10. Model Registry:** `{doc.model_registry}`")
    
    st.markdown("---")
    
    # Layer-Specific Visual/Metric Logic
    if layer in ["Strategic", "Executive"]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Financial: Projected Margin", "+2.4%", "Optimized")
        c2.metric("Customer: NPS Delta", "+8 pts", "Trend alignment")
        c3.metric("Risk: Fraud/Error Rate", "0.01%", "-0.05%")
    elif layer == "Technical":
        st.info("System Architecture Status: All upstream systems responding nominally. Data lineage verified.")
    elif "Design" in persona or "Content" in persona:
        st.subheader("Visual Asset Generation")
        cols = st.columns(3)
        for i in range(3):
            cols[i].image(f"https://source.unsplash.com/featured/400x400?{sub_ind.split()[0].lower()},{domain.split()[0].lower()}&sig={i}", caption=f"Semantic Concept {i+1}")

    # Output the LLM Insights
    st.markdown(st.session_state.intel)

    # Follow-up Chat
    st.markdown("---")
    st.subheader(f"💬 Query Semantic Layer ({domain})")
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])
    
    if prompt := st.chat_input("Ask a follow-up about the data..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            chat_context = f"Base Intelligence: {st.session_state.intel}\nScrape: {st.session_state.scrape_doc}\nUser: {prompt}"
            r = client.chat.completions.create(
                messages=[{"role": "user", "content": chat_context}],
                model="llama-3.1-8b-instant"
            ).choices[0].message.content
            st.markdown(r)
            st.session_state.chat_history.append({"role": "assistant", "content": r})
