import streamlit as st
import json
import pandas as pd
import urllib.parse
import re
import os
import subprocess
from pydantic import BaseModel
from typing import List, Dict, Any

# --- CORE LIBRARY CHECK ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. Run: pip install groq")
    st.stop()

# ==========================================
# 1. UI & BRANDING SETTINGS (TIGER ANALYTICS)
# ==========================================
st.set_page_config(page_title="Tiger Analytics | Sense & Respond OS", layout="wide", initial_sidebar_state="expanded")

try:
    st.logo("tiger_logo.png", icon_image="tiger_logo.png")
except Exception:
    pass

def inject_studio_aesthetic():
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #FAFAFA;
            color: #1C1C1C;
        }
        header[data-testid="stHeader"] { background-color: #FAFAFA; border-bottom: 2px solid #F5A623; }
        
        h1 { font-size: 2.2rem !important; font-weight: 300 !important; letter-spacing: -0.03em !important; color: #1C1C1C !important; padding-bottom: 0 !important; margin-bottom: 0 !important;}
        h2 { font-size: 1.4rem !important; font-weight: 400 !important; letter-spacing: -0.01em !important; color: #1C1C1C !important; margin-top: 1.5rem !important; margin-bottom: 1rem !important; border-bottom: 1px solid #E5E7EB; padding-bottom: 0.5rem;}
        h3 { font-size: 0.9rem !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; color: #F5A623 !important; margin-bottom: 0.5rem !important; }
        
        [data-testid="column"] { display: flex; flex-direction: column; }
        [data-testid="column"] > div { flex-grow: 1; display: flex; flex-direction: column; }
        
        [data-testid="stVerticalBlockBorderWrapper"] {
            height: 100% !important; border: 1px solid #E5E7EB !important; 
            border-radius: 8px !important; background-color: #FFFFFF !important; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        }
        div[data-testid="stVerticalBlock"] div[style*="border"] { padding: 1.25rem !important; border: none !important; box-shadow: none !important; }

        .stButton>button {
            background-color: #1C1C1C !important; color: #FFFFFF !important; border: none !important; border-radius: 4px !important;
            font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; padding: 0.5rem 1rem !important;
        }
        .stButton>button:hover { background-color: #F5A623 !important; color: #1C1C1C !important; }
        
        .stProgress > div > div > div > div { background-color: #F5A623 !important; height: 6px !important; }
        
        /* Sidebar & Chat Styles */
        [data-testid="stSidebar"] { border-right: 1px solid #E5E7EB; }
        .stChatMessage { background-color: #FFFFFF !important; border: 1px solid #E5E7EB !important; border-radius: 8px !important; padding: 0.8rem !important; font-size: 0.9rem !important; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
    </style>
    """, unsafe_allow_html=True)

inject_studio_aesthetic()

# ==========================================
# 2. PERSONAS & TAXONOMY
# ==========================================
INDUSTRIES = {
    "Retail & Apparel": ["Athleisure & Footwear", "Fast Fashion", "Luxury Apparel"],
    "CPG & FMCG": ["Food & Beverage", "Personal Care", "Household Goods"],
    "Direct-to-Consumer (D2C)": ["Subscription Boxes", "Digital-Native Brands"]
}

PERSONAS = [
    "Creative Designer (Ops)", 
    "Marketing Professional (Ops)", 
    "Merchandiser (Ops)", 
    "Sales Professional (Frontline)",
    "Analyst / Data Scientist (Analytical)",
    "Brand Strategy Leader (Strategy)"
]

# ==========================================
# 3. BACKEND ENGINES: MACRO SENSE & RESPOND
# ==========================================
def simulate_external_scrape(ind: str, sub: str, client: Groq):
    sys_prompt = f"""
    You are an autonomous market anomaly crawler for 2026. Analyze the {sub} sector within {ind}. 
    Return STRICTLY VALID JSON EXACTLY matching this format:
    {{
        "hero_insight": "1-sentence macro trend revelation about bleeding-edge consumer demand.",
        "trending_keywords": {{"Keyword One": 98, "Keyword Two": 85, "Keyword Three": 77}}
    }}
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}, temperature=0.5 
        )
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return {
            "hero_insight": "Consumers are shifting towards hyper-localized, on-demand micro-manufacturing.",
            "trending_keywords": {"Micro-manufacturing": 94, "Hyper-local drops": 89, "Synthetic materials": 82}
        }

def execute_omniverse_synthesis(ind, sub, per, anomaly_data, client: Groq):
    sys_prompt = f"""
    You are an autonomous Agent advising a {per} in the {sub} ({ind}) sector.
    LIVE TREND DATA: {json.dumps(anomaly_data)}

    OUTPUT FORMAT (STRICT JSON):
    {{
        "trend_implication": "string (Why this trend matters financially)",
        "strategic_pillars": [ {{"title": "string", "description": "string"}} ],
        "kpi_impact_matrix": [ {{"kpi_name": "string", "impact_metric": "string", "mckinsey_rationale": "string"}} ],
        "persona_deliverables": [ {{"title": "string", "description": "string"}} ],
        "source_links": [ {{"title": "string", "url": "string"}} ]
    }}
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}, temperature=0.3 
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return None

# ==========================================
# 4. BACKEND ENGINES: MULTIMODAL STUDIO
# ==========================================
def analyze_multimodal_file(persona: str) -> Dict[str, Any]:
    """Simulates Gemini Vision returning strict JSON for the specific persona."""
    try:
        if "Designer" in persona:
            mock_json = '{"style_aesthetic": "Neo-Utility Athleisure", "clothing_items": ["Oversized Cargo Trousers", "Tactical Harness"], "bleeding_signal_detected": "Hyper-functional urban wear driven by unpredictable weather patterns."}'
        elif "Marketing" in persona:
            mock_json = '{"competitor_offer": "20% off sustainable basics", "visual_hook": "High-contrast minimalist typography", "bleeding_signal_detected": "Consumer fatigue with loud branding.", "counter_campaign_draft": {"email_subject_line": "Forget Basics. Discover Verified Authenticity.", "tiktok_hook": "Why everyone is throwing away their generic basics this week..."}}'
        elif "Merchandiser" in persona:
            mock_json = '{"missing_categories": ["Regenerative Materials", "Adaptable Outerwear"], "suggested_rotation": ["Move adaptable outerwear to primary end-cap"], "bleeding_signal_justification": "Micro-climate shifts are driving demand for layers."}'
        elif "Analyst" in persona:
            mock_json = '{"data_summary": "Q3 velocity dropping in legacy categories.", "correlated_bleeding_signals": ["Shift to hyper-local micro-trends"], "missed_opportunities": ["Over-indexing ad spend on saturated legacy SKUs."]}'
        else:
            mock_json = '{"status": "Agentic multimodal sequence completed."}'
        return json.loads(mock_json)
    except json.JSONDecodeError:
        return {"error": "Failed to parse LLM output."}

def execute_backend_script(script_name: str, args: list):
    try:
        if not os.path.exists(script_name):
            st.warning(f"Backend Warning: `{script_name}` not found in directory. Simulating successful execution for demo purposes.")
            return True
        subprocess.run(["python", script_name] + args, capture_output=True, text=True, check=True)
        return True
    except Exception as e:
        st.error(f"Backend Error: {e}")
        return False

# ==========================================
# 5. STATE MANAGEMENT
# ==========================================
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "multimodal_context" not in st.session_state: st.session_state.multimodal_context = None
if "scraped_data" not in st.session_state: st.session_state.scraped_data = None
if "auto_intelligence_generated" not in st.session_state: st.session_state.auto_intelligence_generated = None
if "vto_output" not in st.session_state: st.session_state.vto_output = None
if "imagen_output" not in st.session_state: st.session_state.imagen_output = None

# ==========================================
# 6. SIDEBAR: COMMAND CENTER & CHAT
# ==========================================
with st.sidebar:
    st.markdown("### 🎛️ OS Parameters")
    sel_ind = st.selectbox("Industry", list(INDUSTRIES.keys()))
    sel_sub = st.selectbox("Sub-Industry", INDUSTRIES[sel_ind])
    sel_per = st.selectbox("Agentic Persona", PERSONAS)
    
    st.markdown("### 📎 Multimodal Studio Input")
    st.caption("Upload Images/CSVs to trigger dynamic Generative Actions.")
    uploaded_files = st.file_uploader("Upload Assets", accept_multiple_files=True, type=['png','jpg','jpeg','csv','txt'])
    
    if st.button("Execute Sense & Respond Sequence", type="primary", use_container_width=True):
        with st.spinner("SENSE PHASE: Scanning anomalies & processing uploads..."):
            
            # Reset Visual Outputs
            st.session_state.vto_output = None
            st.session_state.imagen_output = None
            
            # 1. Macro Sense Engine
            sd = simulate_external_scrape(sel_ind, sel_sub, client)
            st.session_state.scraped_data = sd
            
            # 2. Macro Strategy Engine
            intel = execute_omniverse_synthesis(sel_ind, sel_sub, sel_per, sd, client)
            st.session_state.auto_intelligence_generated = intel
            
            # 3. Multimodal Studio Engine
            if uploaded_files:
                is_csv = any(f.name.endswith('csv') for f in uploaded_files)
                st.session_state.multimodal_context = {
                    "files": uploaded_files, 
                    "json_analysis": analyze_multimodal_file(sel_per)
                }
            else:
                st.session_state.multimodal_context = None
                
            st.session_state.chat_history = [{"role": "assistant", "content": f"Sequence executed for {sel_per.split(' ')[0]}. OS ready for queries."}]

    st.divider()
    
    st.markdown("### 💬 OS Terminal")
    chat_container = st.container(height=350)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    if prompt := st.chat_input("Query assets or adjust strategy..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    resp = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a conversational OS agent. Be professional and concise."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile", temperature=0.4
                    )
                    content = re.sub(r'<think>.*?</think>', '', resp.choices[0].message.content, flags=re.DOTALL).strip()
                    st.markdown(content)
                    st.session_state.chat_history.append({"role": "assistant", "content": content})
                except Exception as e:
                    st.error(f"Chat Error: {e}")

# ==========================================
# 7. MAIN PANE: UNIFIED OS DASHBOARD
# ==========================================
st.title("Tiger Analytics | Marketing Sense & Respond OS")

if not st.session_state.auto_intelligence_generated:
    st.markdown("""
        <div style='padding: 4rem 2rem; color: #49494A; border: 2px dashed #E5E7EB; border-radius: 8px;'>
            <h2 style='border: none; margin-bottom: 0.5rem;'>System Initialization Required</h2>
            <p style='font-size: 1.1rem; font-weight: 300;'>Configure your parameters in the sidebar. Optionally upload Multimodal assets (Images/CSVs) to unlock the Generative Studio tools. Click <strong>Execute Sequence</strong> to begin.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    doc = st.session_state.auto_intelligence_generated
    sd = st.session_state.scraped_data

    # --- BLOCK 1: MACRO BLEEDING SIGNAL ---
    st.markdown(f"""
        <div style='background-color:#FFFFFF; border:1px solid #E5E7EB; padding:1.25rem; margin-bottom:1.5rem; border-left:4px solid #F5A623; border-radius: 4px;'>
            <div style='font-weight:700; color:#F5A623; font-size:0.85rem; text-transform:uppercase; margin-bottom:0.5rem;'>Bleeding-Edge Signal Detected</div>
            <div style='font-size:1.2rem; font-weight:300; line-height:1.5; color:#1C1C1C;'>{sd.get('hero_insight', 'Market shift detected.')}</div>
        </div>
    """, unsafe_allow_html=True)

    # --- BLOCK 2: TRENDS & "SO WHAT" ---
    col_trends, col_implication = st.columns([1, 1.5], gap="large")
    with col_trends:
        with st.container(border=True):
            st.markdown("### Top Trending Signals")
            for kw, score in sd.get("trending_keywords", {}).items():
                try:
                    safe_score = min(max(int(score), 0), 100)
                    st.markdown(f"<div style='margin-bottom:-10px; font-weight:600; font-size:0.85rem;'>{str(kw).title()} <span style='float:right; color:#F5A623;'>{safe_score}%</span></div>", unsafe_allow_html=True)
                    st.progress(safe_score / 100.0)
                except ValueError: continue

    with col_implication:
        with st.container(border=True):
            st.markdown("### The 'So What?' (Virality Implication)")
            st.markdown(f"<span style='color:#49494A; font-size:1rem; font-weight:300; line-height:1.6;'>{doc.get('trend_implication', '')}</span>", unsafe_allow_html=True)

    # --- BLOCK 3: MECE PILLARS ---
    st.markdown("<h2>Actionable Strategy</h2>", unsafe_allow_html=True)
    pillars = doc.get('strategic_pillars', [])
    if pillars:
        cols = st.columns(len(pillars), gap="large")
        for i, pillar in enumerate(pillars):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### 0{i+1} : {pillar.get('title', '').upper()}")
                    st.markdown(f"<span style='color:#49494A; font-size:0.95rem; font-weight:300;'>{pillar.get('description', '')}</span>", unsafe_allow_html=True)

    st.divider()

    # --- BLOCK 4: AGENTIC MULTIMODAL STUDIO (INJECTED ADDITION) ---
    if st.session_state.multimodal_context:
        st.markdown("<h2>Agentic Multimodal Studio</h2>", unsafe_allow_html=True)
        files = st.session_state.multimodal_context["files"]
        ctx_json = st.session_state.multimodal_context["json_analysis"]
        
        with st.container(border=True):
            # 1. DESIGNER
            if "Designer" in sel_per and any(f.name.endswith(('png', 'jpg')) for f in files):
                c1, c2 = st.columns([1, 1.5], gap="large")
                with c1:
                    st.markdown("### Aesthetic Blueprint (JSON)")
                    st.json(ctx_json)
                    if st.button("Generate Production Image (Imagen 3)", use_container_width=True):
                        if execute_backend_script("scripts/generate_trend_image.py", ["--influencer-id", "auto", "--trend-id", "latest"]):
                            st.session_state.imagen_output = "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&q=80&w=800"
                            st.rerun()
                with c2:
                    if st.session_state.imagen_output:
                        st.image(st.session_state.imagen_output, caption="Imagen 3 Synthesis", use_container_width=True)
                    else:
                        st.info("Awaiting Imagen 3 execution.")

            # 2. MARKETING
            elif "Marketing" in sel_per and any(f.name.endswith(('png', 'jpg')) for f in files):
                st.markdown("### Competitor Deconstruction")
                st.markdown(f"**Target Offer:** {ctx_json.get('competitor_offer', 'N/A')}")
                st.markdown(f"**Visual Hook:** {ctx_json.get('visual_hook', 'N/A')}")
                draft = ctx_json.get("counter_campaign_draft", {})
                st.markdown(f"**Suggested Counter-Hook:** *\"{draft.get('tiktok_hook', 'N/A')}\"*")

            # 3. MERCHANDISER
            elif "Merchandiser" in sel_per and any(f.name.endswith(('png', 'jpg')) for f in files):
                st.markdown("### Planogram Intelligence")
                st.markdown(f"**Missing Categories:** {', '.join(ctx_json.get('missing_categories', []))}")
                st.markdown(f"**Rotation Action:** {', '.join(ctx_json.get('suggested_rotation', []))}")

            # 4. SALES (VTO)
            elif "Sales" in sel_per:
                if len(files) == 2:
                    c1, c2 = st.columns([1, 2], gap="large")
                    with c1:
                        st.markdown("### Google VTO Pipeline")
                        st.caption(f"Source: {files[0].name} | Ref: {files[1].name}")
                        if st.button("Run Virtual Try-On API", use_container_width=True):
                            with st.spinner("Processing via Google Cloud..."):
                                if execute_backend_script("scripts/run_virtual_tryon.py", ["--source", files[0].name, "--reference", files[1].name, "--output-dir", "./out"]):
                                    st.session_state.vto_output = "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&q=80&w=800"
                                    st.rerun()
                    with c2:
                        if st.session_state.vto_output:
                            st.image(st.session_state.vto_output, caption="Google VTO Output", use_container_width=True)
                else:
                    st.warning("Virtual Try-On requires exactly TWO images uploaded (Source + Reference).")

            # 5. ANALYST
            elif "Analyst" in sel_per and any(f.name.endswith('csv') for f in files):
                st.markdown("### Data Synthesis")
                st.markdown(f"**Insight:** {ctx_json.get('data_summary', 'N/A')}")
                try:
                    csv_file = next(f for f in files if f.name.endswith('csv'))
                    df = pd.read_csv(csv_file)
                    st.dataframe(df.head(5), use_container_width=True)
                    if len(df.columns) >= 2:
                        st.bar_chart(df.iloc[:, [0, 1]].set_index(df.columns[0]), color="#F5A623")
                except Exception:
                    st.error("Error rendering CSV.")
            else:
                st.info("Files ingested into context memory. Ready for chat querying.")
        st.divider()

    # --- BLOCK 5: FUNCTIONAL PREDICTABLE DELIVERABLES ---
    st.markdown(f"<h2>Functional Execution Assets: {sel_per.split(' ')[0]}</h2>", unsafe_allow_html=True)
    deliverables = doc.get('persona_deliverables', [])
    if deliverables:
        del_cols = st.columns(len(deliverables), gap="large")
        for i, item in enumerate(deliverables):
            with del_cols[i]:
                with st.container(border=True):
                    if any(role in sel_per for role in ["Designer", "Marketing", "Merchandiser"]):
                        raw_title = item.get('title', 'concept')
                        clean_terms = re.sub(r'[^a-zA-Z\s]', '', raw_title).strip().replace(' ', ',')
                        img_url = f"https://loremflickr.com/600/400/pinterest,aesthetic,{clean_terms}?lock={i+150}"
                        st.markdown(f'<img src="{img_url}" style="width: 100%; border-radius: 4px; margin-bottom: 12px; border: 1px solid #E5E7EB;">', unsafe_allow_html=True)
                        
                    st.markdown(f"**{item.get('title', 'Asset')}**")
                    st.markdown(f"<span style='color:#49494A; font-size:0.9rem; font-weight:300;'>{item.get('description', '')}</span>", unsafe_allow_html=True)

    st.divider()
    
    # --- BLOCK 6: KPI IMPACT & RATIONALE ---
    if "Designer" not in sel_per:
        st.markdown("<h2>Core KPI Impact & Economic Rationale</h2>", unsafe_allow_html=True)
        kpi_matrix = doc.get('kpi_impact_matrix', [])
        if kpi_matrix:
            kpi_cols = st.columns(len(kpi_matrix) or 1, gap="large")
            for i, kpi in enumerate(kpi_matrix):
                with kpi_cols[i % len(kpi_cols)]:
                    with st.container(border=True):
                        st.markdown(f"""
                            <div style='font-size: 0.8rem; font-weight: 700; color: #F5A623; text-transform: uppercase; line-height: 1.2; margin-bottom: 0.5rem;'>
                                {kpi.get('kpi_name', 'KPI')}
                            </div>
                            <div style='font-size: 2.2rem; font-weight: 300; color: #1C1C1C; margin-bottom: 0.5rem;'>
                                {kpi.get('impact_metric', '0%')}
                            </div>
                            <div style='font-size: 0.95rem; font-weight: 300; color: #49494A; line-height: 1.5;'>
                                {kpi.get('mckinsey_rationale', '')}
                            </div>
                        """, unsafe_allow_html=True)
        st.divider()

    # --- SOURCES ---
    st.markdown("<h2>Epistemic Origins & Sources</h2>", unsafe_allow_html=True)
    sources = doc.get('source_links', [])
    if sources:
        src_cols = st.columns(len(sources) if len(sources) > 0 else 1, gap="large")
        for i, src in enumerate(sources):
            with src_cols[i % len(src_cols)]:
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
