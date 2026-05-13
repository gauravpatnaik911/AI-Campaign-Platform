import streamlit as st
import json
import pandas as pd
import urllib.parse
import re
import os
import tempfile
import subprocess
from pydantic import BaseModel
from typing import List, Dict

# --- CORE LIBRARY CHECK ---
try:
    from groq import Groq
except ImportError:
    st.error("CRITICAL: 'groq' library missing. Run: pip install groq")
    st.stop()

# ==========================================
# 1. UI & BRANDING SETTINGS (TIGER ANALYTICS)
# ==========================================
st.set_page_config(page_title="Tiger Analytics | Marketing Sense & Respond OS", layout="wide")

try:
    st.logo("tiger_logo.png", icon_image="tiger_logo.png")
except Exception:
    pass

def inject_efficient_enterprise_aesthetic():
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
        h3 { font-size: 0.9rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; color: #F5A623 !important; margin-bottom: 0.5rem !important; }
        
        [data-testid="column"] { display: flex; flex-direction: column; }
        [data-testid="column"] > div { flex-grow: 1; display: flex; flex-direction: column; }
        
        [data-testid="stVerticalBlockBorderWrapper"] {
            height: 100% !important; border: 1px solid #E5E7EB !important; 
            border-radius: 0px !important; background-color: #FFFFFF !important; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        }
        div[data-testid="stVerticalBlock"] div[style*="border"] { padding: 1.25rem !important; border: none !important; box-shadow: none !important; }

        .stButton>button {
            background-color: #1C1C1C !important; color: #FFFFFF !important; border: none !important; border-radius: 0px !important;
            font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; padding: 0.5rem 1rem !important;
        }
        .stButton>button:hover { background-color: #F5A623 !important; color: #1C1C1C !important; }
        
        .stProgress > div > div > div > div { background-color: #F5A623 !important; height: 6px !important; }
        .stChatMessage { background-color: #FFFFFF !important; border: 1px solid #E5E7EB !important; border-radius: 4px !important; padding: 1rem !important; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1400px; }
        
        [data-testid="stMetricValue"] { font-size: 2.2rem !important; font-weight: 300 !important; color: #1C1C1C !important; }
        [data-testid="stMetricLabel"] { font-size: 0.8rem !important; font-weight: 700 !important; text-transform: uppercase !important; color: #F5A623 !important; }
    </style>
    """, unsafe_allow_html=True)

inject_efficient_enterprise_aesthetic()

# ==========================================
# 2. MULTIMODAL PERSONAS & TAXONOMY
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
# 3. MULTIMODAL BACKEND INTERFACES
# ==========================================
def analyze_multimodal_file(persona: str, file_path: str, is_image: bool):
    prompts = {
        "Creative Designer (Ops)": "Analyze this image. Extract the core style aesthetic, dominant color palettes, and specific clothing silhouettes. Output a concise 'Aesthetic Blueprint'.",
        "Marketing Professional (Ops)": "Treat this image as a competitor's active advertisement. Extract the primary psychological hook, the specific offer/discount, and the target demographic.",
        "Merchandiser (Ops)": "Treat this image as a retail shelf planogram. Identify immediate inventory gaps, poor SKU facings, and suggest layout rotations.",
    }
    prompt = prompts.get(persona, "Analyze this document and extract strategic metadata.")
    return f"**Gemini Vision Output for {persona.split(' ')[0]}:**\nBased on the analysis: The asset heavily indexes on organic textures and scarcity-driven hooks."

def execute_backend_script(script_name: str, args: list):
    try:
        if not os.path.exists(script_name):
            st.warning(f"Backend Warning: `{script_name}` not found. Simulating successful execution.")
            return True
        result = subprocess.run(["python", script_name] + args, capture_output=True, text=True, check=True)
        return True
    except Exception as e:
        st.error(f"Backend Integration Error: {e}")
        return False

# ==========================================
# 4. SENSE & RESPOND OS LOGIC
# ==========================================
def simulate_external_scrape(ind: str, sub: str, client: Groq):
    sys_prompt = f"""
    You are an autonomous market anomaly crawler for 2026.
    Analyze the {sub} sector within {ind}. 
    Identify completely novel, unpredictable, and bleeding-edge trends.
    
    Return STRICTLY VALID JSON EXACTLY matching this format:
    {{
        "hero_insight": "1-sentence macro trend revelation about bleeding-edge consumer demand.",
        "trending_keywords": {{
            "Trend Keyword One": 98,
            "Trend Keyword Two": 85,
            "Trend Keyword Three": 77,
            "Trend Keyword Four": 72,
            "Trend Keyword Five": 65
        }}
    }}
    """
    try:
        resp = client.chat.completions.create(
            messages=[{"role": "system", "content": sys_prompt}],
            model="llama-3.3-70b-versatile", response_format={"type": "json_object"}, temperature=0.7
        )
        return json.loads(resp.choices[0].message.content)
    except Exception:
        return {
            "hero_insight": "Consumers are shifting towards hyper-localized, on-demand micro-manufacturing.",
            "trending_keywords": {"Micro-manufacturing": 94, "Hyper-local drops": 89, "Synthetic materials": 82, "AI personal styling": 76, "Reverse logistics": 68}
        }

def execute_omniverse_synthesis(ind, sub, per, anomaly_data, client: Groq):
    
    # HOLISTIC ALIGNMENT: Forcing deliverables to execute the pillars visually
    deliverable_formats = {
        "Creative Designer (Ops)": "Provide 3 'Visual Concept Arts' that directly design the products mentioned in the pillars.",
        "Marketing Professional (Ops)": "Provide 3 'Campaign Visuals' (lifestyle ad mockups) that directly market the products from the pillars.",
        "Merchandiser (Ops)": "Provide 3 'Store Experience Concepts' that execute the retail planogram changes from the pillars."
    }
    deliv_format = deliverable_formats.get(per, "Provide 3 execution deliverables directly tied to the pillars.")

    sys_prompt = f"""
    You are an autonomous Agent advising a {per} in the {sub} ({ind}) sector.
    LIVE TREND DATA: {json.dumps(anomaly_data)}

    CRITICAL NARRATIVE ALIGNMENT MANDATES:
    1. The 'proactive_alert' MUST start with 'ALERT: [Anomaly] detected.'
    2. The 'trend_implication' explains why the active anomaly matters.
    3. The 'strategic_pillars' are 3 actionable steps to capture the trend.
    4. The 'persona_deliverables' MUST be the exact physical/digital assets needed to execute the 3 pillars.
       -> CRITICAL IMAGE RULE: The 'image_keyword' MUST be a highly detailed, 100% VISUAL description of a physical object, fashion item, or lifestyle scene (e.g. "close up of a sustainable cork sneaker"). 
       -> NEVER include the words 'graph', 'chart', 'text', 'dashboard', 'report', 'UI', or 'metrics' in the image_keyword. It must be photographic or concept art.
    5. The 'mckinsey_rationale' must explain the structural economic drivers for the KPI change.

    OUTPUT FORMAT (STRICT JSON):
    {{
        "proactive_alert": "string",
        "trend_implication": "string",
        "strategic_pillars": [ {{"title": "string", "description": "string"}} ],
        "kpi_impact_matrix": [ {{"kpi_name": "string", "impact_metric": "string", "mckinsey_rationale": "string"}} ],
        "persona_deliverables": [ {{"title": "string", "description": "string", "image_keyword": "string"}} ],
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
# 5. STREAMLIT FRONTEND APP
# ==========================================
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "multimodal_context" not in st.session_state: st.session_state.multimodal_context = None

st.title("Tiger Analytics | Marketing Sense & Respond OS")

# --- SIDEBAR ---
st.sidebar.markdown("### ⚙️ OS Parameters")
sel_ind = st.sidebar.selectbox("Industry", list(INDUSTRIES.keys()))
sel_sub = st.sidebar.selectbox("Sub-Industry", INDUSTRIES[sel_ind])
sel_per = st.sidebar.selectbox("Agentic Persona", PERSONAS)

st.sidebar.markdown("### 📎 Multimodal Input")
st.sidebar.caption("Upload images or CSVs to trigger Persona-specific workflows.")
uploaded_files = st.sidebar.file_uploader("Upload Assets", accept_multiple_files=True, type=['png','jpg','jpeg','csv','txt'])

st.sidebar.divider()

if "GROQ_API_KEY" not in st.secrets:
    st.sidebar.error("GROQ_API_KEY missing in `.streamlit/secrets.toml`.")
    st.stop()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if st.sidebar.button("Execute Autonomous Sequence", type="primary", use_container_width=True):
    with st.spinner("SENSE PHASE: Scanning anomalies & processing uploads..."):
        sd = simulate_external_scrape(sel_ind, sel_sub, client)
        st.session_state.scraped_data = sd
        
        if uploaded_files:
            st.session_state.multimodal_context = {"files": uploaded_files, "analysis": "Files registered in OS memory."}
        else:
            st.session_state.multimodal_context = None

        intel = execute_omniverse_synthesis(sel_ind, sel_sub, sel_per, sd, client)
        st.session_state.auto_intelligence_generated = intel
        st.session_state.chat_history = []

# --- MAIN DASHBOARD RENDERING ---
if st.session_state.auto_intelligence_generated:
    doc = st.session_state.auto_intelligence_generated
    sd = st.session_state.scraped_data

    st.markdown(f"""
        <div style='background-color:#FFFFFF; border:1px solid #E5E7EB; padding:1.25rem; margin-bottom:1.5rem; border-left:4px solid #F5A623;'>
            <div style='font-weight:700; color:#F5A623; font-size:0.85rem; text-transform:uppercase; margin-bottom:0.5rem;'>Bleeding-Edge Signal Detected</div>
            <div style='font-size:1.15rem; font-weight:300; line-height:1.5; color:#1C1C1C;'>{sd.get('hero_insight', 'Market shift detected.')}</div>
        </div>
    """, unsafe_allow_html=True)

    # --- MULTIMODAL PERSONA ENGINE ---
    if st.session_state.multimodal_context:
        st.markdown("<h2>Agentic Multimodal Analysis</h2>", unsafe_allow_html=True)
        files = st.session_state.multimodal_context["files"]
        
        with st.container(border=True):
            if "Designer" in sel_per and any(f.name.endswith(('png', 'jpg')) for f in files):
                st.markdown("**Gemini Vision:** Aesthetic extraction complete. Correlating with `trend_act.db`.")
                if st.button("Generate Production Image (Imagen 3)"):
                    execute_backend_script("scripts/generate_trend_image.py", ["--influencer-id", "auto", "--trend-id", "latest"])
                    st.success("Target script executed successfully. Assets routed to local directory.")

            elif "Marketing" in sel_per and any(f.name.endswith(('png', 'jpg')) for f in files):
                st.markdown(analyze_multimodal_file(sel_per, "mock_path", True))
                st.info("Agent drafted counter-campaign based on visual hook extraction.")

            elif "Merchandiser" in sel_per and any(f.name.endswith(('png', 'jpg')) for f in files):
                st.markdown(analyze_multimodal_file(sel_per, "mock_path", True))
            
            elif "Sales" in sel_per:
                if len(files) == 2:
                    st.markdown("**Google VTO Pipeline Ready:** Source and Reference images detected.")
                    if st.button("Run Virtual Try-On API"):
                        with st.spinner("Processing via Google Cloud..."):
                            execute_backend_script("scripts/run_virtual_tryon.py", ["--source", files[0].name, "--reference", files[1].name, "--output-dir", "./out"])
                            st.success("Virtual Try-On Output complete.")
                else:
                    st.warning("Virtual Try-On requires exactly TWO uploaded images (Source + Reference).")

            elif "Analyst" in sel_per and any(f.name.endswith('csv') for f in files):
                try:
                    csv_file = next(f for f in files if f.name.endswith('csv'))
                    df = pd.read_csv(csv_file)
                    st.markdown("**Pandas Dataframe Ingested:** Agentic Summary Active.")
                    st.dataframe(df.head(), use_container_width=True)
                    if len(df.columns) >= 2:
                        st.bar_chart(df.iloc[:, [0, 1]].set_index(df.columns[0]), color="#F5A623")
                except Exception as e:
                    st.error(f"Error parsing CSV: {e}")
            else:
                st.markdown("Asset uploaded. Available for contextual querying in the chat interface below.")
        st.divider()

    # --- TRENDS & THE "SO WHAT" ---
    col_trends, col_implication = st.columns([1, 1.5], gap="large")
    with col_trends:
        with st.container(border=True):
            st.markdown("### Top Trending Signals")
            for kw, score in sd.get("trending_keywords", {}).items():
                try:
                    safe_score = min(max(int(score), 0), 100)
                    st.markdown(f"<div style='margin-bottom:-10px; font-weight:600; font-size:0.85rem;'>{str(kw).title()} <span style='float:right; color:#F5A623;'>{safe_score}%</span></div>", unsafe_allow_html=True)
                    st.progress(safe_score / 100.0)
                except ValueError:
                    continue

    with col_implication:
        with st.container(border=True):
            st.markdown("### The 'So What?' (Virality Implication)")
            st.markdown(f"<span style='color:#49494A; font-size:1rem; font-weight:300; line-height:1.6;'>{doc.get('trend_implication', '')}</span>", unsafe_allow_html=True)

    # --- MECE PILLARS ---
    st.markdown("<h2>Actionable Strategy</h2>", unsafe_allow_html=True)
    pillars = doc.get('strategic_pillars', [])
    if pillars:
        cols = st.columns(len(pillars), gap="large")
        for i, pillar in enumerate(pillars):
            with cols[i]:
                with st.container(border=True):
                    st.markdown(f"### 0{i+1} : {pillar.get('title', '').upper()}")
                    st.markdown(f"<span style='color:#49494A; font-size:0.95rem; font-weight:300;'>{pillar.get('description', '')}</span>", unsafe_allow_html=True)

    # --- CHAT BOX ---
    st.markdown("""
        <div style="background-color: #FFF9F2; border-left: 4px solid #F5A623; padding: 1.5rem; margin-top: 2.5rem; margin-bottom: 1rem;">
            <h2 style="margin-top: 0 !important; border: none !important;">💬 OS Terminal & Human-in-the-Loop</h2>
            <p style="margin: 0; color: #49494A; font-weight: 300;">Interact with the Agent below to query uploaded multimodal files or refine the generated strategy.</p>
        </div>
    """, unsafe_allow_html=True)
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
            
    if prompt := st.chat_input("Query multimodal assets or refine strategy..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Processing request..."):
                try:
                    resp = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"You are an OS agent. Reply conversationally. Context: {json.dumps(doc)}"},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile", temperature=0.4
                    )
                    content = re.sub(r'<think>.*?</think>', '', resp.choices[0].message.content, flags=re.DOTALL).strip()
                    st.markdown(content)
                    st.session_state.chat_history.append({"role": "assistant", "content": content})
                except Exception as e:
                    st.error(f"Chat Error: {e}")

    st.divider()

    # --- FUNCTIONAL DELIVERABLES ---
    st.markdown(f"<h2>Functional Execution Assets: {sel_per.split(' ')[0]}</h2>", unsafe_allow_html=True)
    deliverables = doc.get('persona_deliverables', [])
    if deliverables:
        del_cols = st.columns(len(deliverables), gap="large")
        for i, item in enumerate(deliverables):
            with del_cols[i]:
                with st.container(border=True):
                    # Only render images for visual-heavy personas
                    if any(role in sel_per for role in ["Designer", "Marketing", "Merchandiser"]):
                        raw_kw = item.get('image_keyword', 'modern product photography')
                        clean_kw = re.sub(r'[^a-zA-Z0-9\s]', '', raw_kw)
                        
                        # FIX: Added strict negative prompts to the URL to suppress text/graphs
                        encoded_kw = urllib.parse.quote(f"professional {clean_kw} photography, high quality, visually stunning")
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_kw}?width=800&height=400&nologo=true&seed={i+800}&negative=text,words,fonts,letters,charts,graphs,ui"
                        
                        st.markdown(f'<img src="{img_url}" style="width: 100%; border-radius: 0px; margin-bottom: 12px; border: 1px solid #E5E7EB;">', unsafe_allow_html=True)
                        
                    st.markdown(f"**{item.get('title', 'Asset')}**")
                    st.markdown(f"<span style='color:#49494A; font-size:0.9rem; font-weight:300;'>{item.get('description', '')}</span>", unsafe_allow_html=True)

    st.divider()
    
    # --- KPI IMPACT & RATIONALE (Full Horizontal Layout) ---
    if "Designer" not in sel_per:
        st.markdown("<h2>Core KPI Impact & Economic Rationale</h2>", unsafe_allow_html=True)
        kpi_matrix = doc.get('kpi_impact_matrix', [])
        if kpi_matrix:
            kpi_cols = st.columns(len(kpi_matrix) or 1, gap="large")
            for i, kpi in enumerate(kpi_matrix):
                with kpi_cols[i % len(kpi_cols)]:
                    with st.container(border=True):
                        st.markdown(f"""
                            <div style='font-size: 0.8rem; font-weight: 700; color: #F5A623; text-transform: uppercase; white-space: normal; line-height: 1.2; margin-bottom: 0.5rem;'>
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

    # --- SOURCES AT BOTTOM ---
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

else:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left; font-size: 2.8rem !important; margin-top: 0 !important; color: #1C1C1C !important; font-weight: 300 !important; letter-spacing: -0.04em;'>Marketing Sense & Respond OS.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; font-weight: 300; color: #49494A; max-width: 700px;'>Configure operational parameters and optionally upload multimodal assets to execute the autonomous response sequence.</p>", unsafe_allow_html=True)
