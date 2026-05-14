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
# 1. UI & BRANDING SETTINGS (SENSE AI CSS)
# ==========================================
st.set_page_config(page_title="Tiger Analytics | Sense & Respond", layout="wide", initial_sidebar_state="expanded")

try:
    st.logo("tiger_logo.png", icon_image="tiger_logo.png")
except Exception:
    pass

def inject_studio_aesthetic():
    st.markdown("""
    <style>
        /* CSS Variables from Reimagine BI */
        :root {
            --primary-orange: #f48221;
            --sidebar-bg: #fdf8f4;
            --card-bg: #ffffff;
            --main-bg: #f5f5f5;
            --text-main: #333333;
            --text-muted: #666666;
            --border-color: #eeeeee;
        }

        /* Base Reset */
        html, body, [class*="css"] {
            font-family: 'Inter', "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: var(--main-bg);
            color: var(--text-main);
        }
        
        /* Top Header & Sidebar */
        header[data-testid="stHeader"] { background-color: var(--primary-orange); border-bottom: none; height: 50px;}
        [data-testid="stSidebar"] { background-color: var(--sidebar-bg) !important; border-right: 1px solid var(--border-color); }
        [data-testid="stAppViewContainer"] { background-color: var(--main-bg); }
        
        /* Typography */
        h1 { font-size: 2rem !important; font-weight: 700 !important; color: var(--text-main) !important; margin-bottom: 0.5rem !important;}
        h2 { font-size: 1.2rem !important; font-weight: 600 !important; color: var(--text-main) !important; margin-top: 1rem !important; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;}
        h3 { font-size: 0.85rem !important; font-weight: 700 !important; color: var(--text-muted) !important; margin-bottom: 0.5rem !important; }
        
        /* Cards */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--border-color) !important; 
            border-radius: 12px !important; 
            background: var(--card-bg) !important; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
            height: 100% !important;
        }
        div[data-testid="stVerticalBlock"] div[style*="border"] { padding: 20px !important; border: none !important; box-shadow: none !important; }

        /* Buttons */
        .stButton>button {
            background-color: var(--card-bg) !important; color: var(--text-main) !important; border: 1px solid var(--primary-orange) !important; border-radius: 8px !important;
            font-weight: 600 !important; padding: 0.5rem 1rem !important;
        }
        .stButton>button:hover { background-color: var(--primary-orange) !important; color: #FFFFFF !important; }
        
        .stProgress > div > div > div > div { background-color: var(--primary-orange) !important; height: 8px !important; }
        .stChatMessage { background-color: #FFFFFF !important; border: 1px solid var(--border-color) !important; border-radius: 8px !important; }
        .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1600px; }
        
        /* Right Panel Chat specific styling */
        .chat-panel { background: #f9f9f9; padding: 20px; border-radius: 12px; border: 1px solid var(--border-color); height: 100%;}
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
    "Supply Chain Manager (Ops)",
    "Analyst / Data Scientist (Analytical)",
    "Brand Strategy Leader (Strategy)"
]

# ==========================================
# 3. BACKEND ENGINES
# ==========================================
def simulate_external_scrape(ind: str, sub: str, client: Groq):
    sys_prompt = f"""
    You are an autonomous market crawler for 2026. Analyze the {sub} sector within {ind}. 
    Return STRICT JSON EXACTLY matching this format:
    {{
        "hero_insight": "1-sentence macro trend revelation.",
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
        "trend_implication": "string (Why this trend matters)",
        "summaryMetrics": [
            {{"label": "string (e.g., DSM Rate)", "value": "string (e.g., 81.7%)", "trend": "string (e.g., -5.70%)", "status": "negative or positive"}}
        ],
        "strategic_pillars": [ {{"title": "string", "description": "string"}} ],
        "persona_deliverables": [ {{"title": "string", "description": "string"}} ],
        "chatQuickStart": ["string (question)", "string", "string"]
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

def analyze_multimodal_file(persona: str) -> Dict[str, Any]:
    try:
        if "Designer" in persona:
            mock_json = '{"style_aesthetic": "Neo-Utility Athleisure", "clothing_items": ["Oversized Cargo Trousers"], "bleeding_signal_detected": "Hyper-functional urban wear."}'
        elif "Marketing" in persona:
            mock_json = '{"competitor_offer": "20% off sustainable basics", "visual_hook": "High-contrast minimalism", "bleeding_signal_detected": "Consumer fatigue with loud branding."}'
        else:
            mock_json = '{"status": "Agentic multimodal sequence completed."}'
        return json.loads(mock_json)
    except:
        return {"error": "Failed"}

def execute_backend_script(script_name: str, args: list):
    try:
        if not os.path.exists(script_name):
            st.warning(f"Backend Warning: `{script_name}` not found. Simulating execution.")
            return True
        subprocess.run(["python", script_name] + args, capture_output=True, text=True, check=True)
        return True
    except Exception as e:
        st.error(f"Backend Error: {e}")
        return False

# ==========================================
# 4. STATE MANAGEMENT
# ==========================================
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "multimodal_context" not in st.session_state: st.session_state.multimodal_context = None
if "scraped_data" not in st.session_state: st.session_state.scraped_data = None
if "auto_intelligence_generated" not in st.session_state: st.session_state.auto_intelligence_generated = None

# ==========================================
# 5. SIDEBAR: NAVIGATION & UPLOADS
# ==========================================
with st.sidebar:
    st.markdown(f"<h3 style='color: var(--text-main) !important;'>Tiger Analytics</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    sel_per = st.selectbox("Role", PERSONAS)
    st.divider()
    
    st.markdown("### Parameters")
    sel_ind = st.selectbox("Industry", list(INDUSTRIES.keys()))
    sel_sub = st.selectbox("Sub-Industry", INDUSTRIES[sel_ind])
    
    st.markdown("### Artifacts")
    uploaded_files = st.file_uploader("Upload Image/CSV", accept_multiple_files=True, type=['png','jpg','jpeg','csv'])
    
    if "GROQ_API_KEY" not in st.secrets:
        st.error("GROQ_API_KEY missing in `.streamlit/secrets.toml`.")
        st.stop()
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Refresh / Execute", use_container_width=True):
        with st.spinner("Processing..."):
            sd = simulate_external_scrape(sel_ind, sel_sub, client)
            st.session_state.scraped_data = sd
            
            intel = execute_omniverse_synthesis(sel_ind, sel_sub, sel_per, sd, client)
            st.session_state.auto_intelligence_generated = intel
            
            if uploaded_files:
                st.session_state.multimodal_context = {"files": uploaded_files, "json_analysis": analyze_multimodal_file(sel_per)}
            else:
                st.session_state.multimodal_context = None
                
            st.session_state.chat_history = [{"role": "assistant", "content": f"Hey there! I've loaded the dashboard for {sel_per.split(' ')[0]}."}]

# ==========================================
# 6. MAIN PANE: SENSE AI DASHBOARD
# ==========================================
if not st.session_state.auto_intelligence_generated:
    st.markdown("""
        <div style='padding: 4rem 2rem; color: var(--text-muted); text-align: center;'>
            <h2>Sense AI Initialization Required</h2>
            <p>Configure parameters in the sidebar and click Refresh to load the OS.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    doc = st.session_state.auto_intelligence_generated
    sd = st.session_state.scraped_data

    # --- SAFETY GUARDRAIL: Prevents AttributeError if cache holds old string data ---
    if not isinstance(doc, dict):
        st.session_state.auto_intelligence_generated = None
        st.warning("🔄 Memory cache conflict detected and cleared. Please click 'Refresh / Execute' again.")
        st.stop()

    # Layout matches the 1fr | 350px CSS grid structure
    col_dash, col_chat = st.columns([3, 1.2], gap="large")

    with col_dash:
        st.markdown(f"<h1>Overview: {sel_per.split(' ')[0]}</h1>", unsafe_allow_html=True)
        
        # --- BLOCK 1: KPI SUMMARY METRICS (From JSON Schema) ---
        metrics = doc.get('summaryMetrics', [])
        if metrics:
            m_cols = st.columns(len(metrics), gap="medium")
            for i, m in enumerate(metrics[:3]): # Max 3 for clean UI
                color = "#d9534f" if m.get("status") == "negative" else "#5cb85c"
                arrow = "↓" if m.get("status") == "negative" else "↑"
                with m_cols[i]:
                    st.markdown(f"""
                        <div style='background: #fff; padding: 15px 20px; border-radius: 12px; border: 1px solid var(--border-color);'>
                            <div style='font-size: 13px; font-weight: 600; color: var(--text-main); margin-bottom: 5px;'>{m.get('label', 'Metric')}</div>
                            <div style='font-size: 26px; font-weight: 700; color: #000; margin-bottom: 2px;'>{m.get('value', '0')}</div>
                            <div style='font-size: 12px; color: {color}; font-weight: 500;'>{arrow} {m.get('trend', '0%')} vs QoQ</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        # --- BLOCK 2: BLEEDING SIGNAL & TRENDS ---
        st.markdown(f"""
            <div style='background-color:#fff; border:1px solid var(--border-color); padding:1.25rem; margin-bottom:1.5rem; border-left:4px solid var(--primary-orange); border-radius: 8px;'>
                <div style='font-weight:700; color:var(--primary-orange); font-size:0.85rem; text-transform:uppercase; margin-bottom:0.5rem;'>Bleeding-Edge Signal</div>
                <div style='font-size:1.1rem; font-weight:400; color:var(--text-main);'>{sd.get('hero_insight', 'Market shift detected.')}</div>
            </div>
        """, unsafe_allow_html=True)

        c_trends, c_imp = st.columns([1, 1.5], gap="large")
        with c_trends:
            with st.container(border=True):
                st.markdown("### Top Trending Keywords")
                for kw, score in sd.get("trending_keywords", {}).items():
                    try:
                        safe_score = min(max(int(score), 0), 100)
                        st.markdown(f"<div style='margin-bottom:-10px; font-weight:600; font-size:0.85rem; color:var(--text-main);'>{str(kw).title()} <span style='float:right; color:var(--primary-orange);'>{safe_score}%</span></div>", unsafe_allow_html=True)
                        st.progress(safe_score / 100.0)
                    except ValueError: continue
        with c_imp:
            with st.container(border=True):
                st.markdown("### Contextual Implication")
                st.markdown(f"<span style='color:var(--text-muted); font-size:0.95rem; line-height:1.6;'>{doc.get('trend_implication', '')}</span>", unsafe_allow_html=True)

        # --- BLOCK 3: AGENTIC MULTIMODAL STUDIO ---
        if st.session_state.multimodal_context:
            st.markdown("<h2>Agentic Assets</h2>", unsafe_allow_html=True)
            files = st.session_state.multimodal_context["files"]
            ctx_json = st.session_state.multimodal_context["json_analysis"]
            
            with st.container(border=True):
                if "Designer" in sel_per and any(f.name.endswith(('png', 'jpg')) for f in files):
                    c1, c2 = st.columns([1, 1.5], gap="large")
                    with c1:
                        st.markdown("### JSON Extraction")
                        st.json(ctx_json)
                        if st.button("Generate Imagen 3", use_container_width=True):
                            st.success("Imagen 3 triggered.")
                elif "Analyst" in sel_per and any(f.name.endswith('csv') for f in files):
                    st.markdown("### Data Synthesis")
                    try:
                        csv_file = next(f for f in files if f.name.endswith('csv'))
                        df = pd.read_csv(csv_file)
                        st.dataframe(df.head(3), use_container_width=True)
                        if len(df.columns) >= 2:
                            st.bar_chart(df.iloc[:, [0, 1]].set_index(df.columns[0]), color="#f48221")
                    except Exception:
                        st.error("Error rendering CSV.")
                else:
                    st.info("Multimodal Context Ingested.")

        # --- BLOCK 4: DELIVERABLES ---
        st.markdown(f"<h2>Functional Deliverables</h2>", unsafe_allow_html=True)
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
                            st.markdown(f'<img src="{img_url}" style="width: 100%; border-radius: 8px; margin-bottom: 12px;">', unsafe_allow_html=True)
                        st.markdown(f"<div style='font-weight:600; font-size:15px; margin-bottom:5px;'>{item.get('title', 'Asset')}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='color:var(--text-muted); font-size:13px;'>{item.get('description', '')}</div>", unsafe_allow_html=True)

    # ==================== RIGHT PANE: CHAT AI ====================
    with col_chat:
        st.markdown("<div class='chat-panel'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-bottom: 20px;'><span style='color:var(--primary-orange);'>🤖 Chat AI</span></h3>", unsafe_allow_html=True)
        
        chat_container = st.container(height=500)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
            
            # Render "Quick Starts" from JSON if history is empty
            if len(st.session_state.chat_history) <= 1:
                st.markdown("<br><div style='font-size: 13px; font-weight: 600; color: var(--text-main); margin-bottom:10px;'>Quick Start</div>", unsafe_allow_html=True)
                for qs in doc.get("chatQuickStart", []):
                    st.markdown(f"""
                        <div style='background: #fff; padding: 10px; border-radius: 6px; border: 1px solid var(--border-color); font-size: 12px; margin-bottom: 8px; cursor: pointer; color: var(--text-muted);'>
                            {qs} <span style='float:right;'>›</span>
                        </div>
                    """, unsafe_allow_html=True)

        if prompt := st.chat_input("Type your query here..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"): st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("..."):
                        try:
                            resp = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": "You are a conversational Sense AI agent."},
                                    {"role": "user", "content": prompt}
                                ],
                                model="llama-3.3-70b-versatile", temperature=0.4
                            )
                            content = re.sub(r'<think>.*?</think>', '', resp.choices[0].message.content, flags=re.DOTALL).strip()
                            st.markdown(content)
                            st.session_state.chat_history.append({"role": "assistant", "content": content})
                        except Exception:
                            pass
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
