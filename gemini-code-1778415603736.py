import streamlit as st
import json
import pandas as pd
import os
import subprocess
import tempfile
from typing import List, Dict, Any

# ==========================================
# 1. UI & BRANDING SETTINGS (THE CREATIVE STUDIO)
# ==========================================
st.set_page_config(page_title="Tiger Analytics | Sense & Respond OS", layout="wide", initial_sidebar_state="expanded")

try:
    # Pinning the logo natively to the top left
    st.logo("tiger_logo.png", icon_image="tiger_logo.png")
except Exception:
    pass

def inject_studio_aesthetic():
    st.markdown("""
    <style>
        /* Base Studio Reset */
        html, body, [class*="css"] {
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #F8F9FA; /* Off-white studio background */
            color: #1C1C1C;
        }
        
        /* Tiger Analytics Orange Header */
        header[data-testid="stHeader"] { background-color: #F8F9FA; border-bottom: 3px solid #F5A623; }
        
        /* Typography */
        h1 { font-size: 2.4rem !important; font-weight: 300 !important; letter-spacing: -0.02em !important; color: #1C1C1C !important; margin-bottom: 0.5rem !important;}
        h2 { font-size: 1.5rem !important; font-weight: 400 !important; letter-spacing: -0.01em !important; color: #1C1C1C !important; margin-top: 1rem !important; border-bottom: 1px solid #E5E7EB; padding-bottom: 0.5rem;}
        h3 { font-size: 0.95rem !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; color: #F5A623 !important; margin-bottom: 0.5rem !important; }
        
        /* Tiger Black/Orange Buttons */
        .stButton>button {
            background-color: #1C1C1C !important; color: #FFFFFF !important; border: none !important; border-radius: 4px !important;
            font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; padding: 0.6rem 1.2rem !important;
            transition: all 0.3s ease;
        }
        .stButton>button:hover { background-color: #F5A623 !important; color: #1C1C1C !important; }
        
        /* Containers: Removing BI Boxiness, emphasizing Canvas feel */
        div[data-testid="stVerticalBlock"] div[style*="border"] {
            border: 1px solid #E5E7EB !important; border-radius: 8px !important; 
            background-color: #FFFFFF !important; padding: 1.5rem !important; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
        }
        
        /* Sidebar Chat Adjustments */
        [data-testid="stSidebar"] { border-right: 1px solid #E5E7EB; }
        .stChatMessage { background-color: #FFFFFF !important; border: 1px solid #E5E7EB !important; border-radius: 8px !important; padding: 0.8rem !important; font-size: 0.9rem !important;}
    </style>
    """, unsafe_allow_html=True)

inject_studio_aesthetic()

# ==========================================
# 2. PERSONAS & TAXONOMY
# ==========================================
PERSONAS = [
    "Creative Designer (Ops)", 
    "Marketing Professional (Ops)", 
    "Merchandiser (Ops)", 
    "Sales Professional (Frontline)",
    "Analyst / Data Scientist (Analytical)",
    "Brand Strategy Leader (Strategy)"
]

# ==========================================
# 3. BACKEND & API WRAPPERS (STRICT JSON)
# ==========================================
def analyze_with_gemini(input_type: str, persona: str, files: list) -> Dict[str, Any]:
    """
    Placeholder for google-genai API calls.
    Returns STRICT JSON strings parsed into dictionaries.
    """
    
    # ---------------------------------------------------------
    # EXACT, HIGH-QUALITY PROMPTS (Strict JSON & Bleeding Signals)
    # ---------------------------------------------------------
    prompts = {
        "Creative Designer (Ops)": """
            Analyze the uploaded image. We are looking for 'Bleeding Signals' (early, high-velocity trends).
            Return STRICTLY VALID JSON EXACTLY matching this format, with no markdown formatting or extra text:
            {
                "style_aesthetic": "string (e.g., Gorpcore, Y2K Cyberpunk)",
                "clothing_items": ["string", "string"],
                "bleeding_signal_detected": "string (Why is this trending right now?)"
            }
        """,
        "Marketing Professional (Ops)": """
            Analyze this competitor ad image. Identify the 'Bleeding Signal' they are attempting to exploit.
            Return STRICTLY VALID JSON EXACTLY matching this format:
            {
                "competitor_offer": "string",
                "visual_hook": "string",
                "bleeding_signal_detected": "string",
                "counter_campaign_draft": {
                    "email_subject_line": "string",
                    "tiktok_hook": "string (Script intro to counter their offer)"
                }
            }
        """,
        "Merchandiser (Ops)": """
            Analyze this retail shelf planogram image. Identify gaps based on current 'Bleeding Signals'.
            Return STRICTLY VALID JSON EXACTLY matching this format:
            {
                "missing_categories": ["string", "string"],
                "suggested_rotation": ["string (What to move to front-cap)"],
                "bleeding_signal_justification": "string"
            }
        """,
        "Analyst / Data Scientist (Analytical)": """
            Analyze the provided CSV data summary. Cross-reference with external 'Bleeding Signals'.
            Return STRICTLY VALID JSON EXACTLY matching this format:
            {
                "data_summary": "string (1 sentence summary)",
                "correlated_bleeding_signals": ["string", "string"],
                "missed_opportunities": ["string (Where is budget being wasted?)"]
            }
        """
    }

    prompt = prompts.get(persona, "Return strict JSON: {'status': 'analyzed'}")
    
    # --- SIMULATING THE GEMINI JSON RESPONSE ---
    # In production: response = model.generate_content([image, prompt]).text
    try:
        if "Designer" in persona:
            mock_json = '{"style_aesthetic": "Neo-Utility Athleisure", "clothing_items": ["Oversized Cargo Trousers", "Tactical Harness"], "bleeding_signal_detected": "Hyper-functional urban wear driven by unpredictable weather patterns."}'
        elif "Marketing" in persona:
            mock_json = '{"competitor_offer": "20% off sustainable basics", "visual_hook": "High-contrast minimalist typography over organic textures", "bleeding_signal_detected": "Consumer fatigue with loud branding; shift to quiet luxury.", "counter_campaign_draft": {"email_subject_line": "Forget Basics. Discover Verified Authenticity.", "tiktok_hook": "Why everyone is throwing away their generic basics this week..."}}'
        elif "Merchandiser" in persona:
            mock_json = '{"missing_categories": ["Regenerative Materials", "Adaptable Outerwear"], "suggested_rotation": ["Move adaptable outerwear to the primary end-cap"], "bleeding_signal_justification": "Micro-climate shifts are driving demand for layers."}'
        elif "Analyst" in persona:
            mock_json = '{"data_summary": "Q3 velocity dropping in legacy categories.", "correlated_bleeding_signals": ["Shift to hyper-local micro-trends"], "missed_opportunities": ["Over-indexing ad spend on saturated legacy SKUs instead of emerging signals."]}'
        else:
            mock_json = '{"status": "Agentic sequence completed."}'
            
        return json.loads(mock_json)
        
    except json.JSONDecodeError as e:
        st.error(f"JSON Parsing Error from Gemini: {e}")
        return {"error": "Failed to parse LLM output."}

def execute_backend_script(script_name: str, args: list):
    """Robust wrapper for local backend scripts."""
    try:
        if not os.path.exists(script_name):
            st.warning(f"Backend Link: `{script_name}` not found. Simulating production execution.")
            return True
        subprocess.run(["python", script_name] + args, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"Execution Failed: {e.stderr}")
        return False
    except Exception as e:
        st.error(f"System Error: {e}")
        return False

# ==========================================
# 4. STATE MANAGEMENT
# ==========================================
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "agent_context" not in st.session_state: st.session_state.agent_context = None
if "generated_image" not in st.session_state: st.session_state.generated_image = None

# ==========================================
# 5. SIDEBAR: COMMAND CENTER & CHAT
# ==========================================
with st.sidebar:
    st.markdown("### 🎛️ Command Center")
    sel_per = st.selectbox("Active Persona", PERSONAS)
    
    st.markdown("### 📎 Multimodal Input")
    uploaded_files = st.file_uploader("Upload Assets (Image/CSV)", accept_multiple_files=True, type=['png','jpg','jpeg','csv','txt'])
    
    if st.button("Initialize Agentic Workflow", use_container_width=True):
        if not uploaded_files and "Strategy" not in sel_per:
            st.warning("Please upload a file to trigger the Multimodal Engine.")
        else:
            with st.spinner(f"Agent synthesizing inputs for {sel_per.split(' ')[0]}..."):
                # Clear previous outputs
                st.session_state.generated_image = None 
                
                # Determine input type
                is_csv = any(f.name.endswith('csv') for f in uploaded_files) if uploaded_files else False
                
                # Call Gemini JSON Wrapper
                st.session_state.agent_context = analyze_with_gemini(
                    input_type="csv" if is_csv else "image",
                    persona=sel_per,
                    files=uploaded_files
                )
                
                # Append system notification to chat
                st.session_state.chat_history.append({"role": "assistant", "content": f"Assets ingested. Bleeding Signal extraction complete for {sel_per.split(' ')[0]}."})

    st.divider()
    
    # --- SIDEBAR CHAT INTERFACE ---
    st.markdown("### 💬 OS Terminal")
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    if prompt := st.chat_input("Query assets or adjust strategy..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        # Mock LLM chat response based on context
        bot_reply = f"Acknowledged. Adapting the Bleeding Signal strategy based on your directive: '{prompt}'."
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()

# ==========================================
# 6. MAIN PANE: GENERATIVE CREATIVE STUDIO
# ==========================================
st.title("Generative Creative Studio")

if not st.session_state.agent_context:
    st.markdown("""
        <div style='text-align: center; padding: 4rem; color: #49494A; border: 2px dashed #E5E7EB; border-radius: 8px;'>
            <h2 style='border: none; margin-bottom: 0;'>Waiting for OS Initialization</h2>
            <p>Select a Persona, upload multimodal assets in the sidebar, and initialize the workflow to populate the studio.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    ctx = st.session_state.agent_context
    files = uploaded_files if uploaded_files else []
    
    # --- Universal Bleeding Signal Header ---
    if "bleeding_signal_detected" in ctx:
        st.markdown(f"""
            <div style='background-color:#FFFFFF; border:1px solid #E5E7EB; padding:1.5rem; margin-bottom:2rem; border-left:5px solid #F5A623; border-radius: 4px;'>
                <div style='font-weight:700; color:#F5A623; font-size:0.85rem; text-transform:uppercase; margin-bottom:0.5rem;'>Detected Bleeding Signal</div>
                <div style='font-size:1.25rem; font-weight:300; line-height:1.5; color:#1C1C1C;'>{ctx['bleeding_signal_detected']}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- 1. DESIGNER LOGIC ---
    if "Designer" in sel_per:
        col1, col2 = st.columns([1, 1.5], gap="large")
        with col1:
            st.markdown("### Aesthetic Blueprint")
            st.json(ctx) # Renders the strictly parsed JSON beautifully
            
            st.markdown("### Agentic Action")
            st.markdown("Querying `trend_act.db` for visual synthesis...")
            if st.button("Generate Production Image (Imagen 3)"):
                with st.spinner("Connecting to Google Cloud Imagen 3..."):
                    success = execute_backend_script("scripts/generate_trend_image.py", ["--influencer-id", "auto", "--trend-id", "latest"])
                    if success:
                        st.session_state.generated_image = "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&q=80&w=800" # High-quality placeholder
                        st.rerun()
        with col2:
            st.markdown("### Studio Canvas")
            if st.session_state.generated_image:
                st.image(st.session_state.generated_image, caption="Imagen 3 Output: Neo-Utility Concept", use_container_width=True)
            else:
                st.info("Canvas empty. Click generate to render the Bleeding Signal aesthetic.")

    # --- 2. MARKETING LOGIC ---
    elif "Marketing" in sel_per:
        col_ad, col_copy = st.columns(2, gap="large")
        with col_ad:
            st.markdown("### Competitor Deconstruction")
            st.markdown(f"**Target Offer:** {ctx.get('competitor_offer', 'N/A')}")
            st.markdown(f"**Visual Hook:** {ctx.get('visual_hook', 'N/A')}")
            st.image("https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=600", caption="Ingested Competitor Asset", use_container_width=True)
            
        with col_copy:
            st.markdown("### Drafted Counter-Campaign")
            draft = ctx.get("counter_campaign_draft", {})
            with st.container(border=True):
                st.markdown(f"**Email Subject Line:**\n\n> *{draft.get('email_subject_line', 'N/A')}*")
            with st.container(border=True):
                st.markdown(f"**TikTok Video Hook Script:**\n\n> *\"{draft.get('tiktok_hook', 'N/A')}\"*")
            st.button("Push to Ad Manager Workflow")

    # --- 3. MERCHANDISER LOGIC ---
    elif "Merchandiser" in sel_per:
        st.markdown("### Planogram Intelligence")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            with st.container(border=True):
                st.markdown("### ⚠️ Missing Categories")
                for cat in ctx.get("missing_categories", []):
                    st.markdown(f"- {cat}")
        with col2:
            with st.container(border=True):
                st.markdown("### 🔄 Suggested Rotation")
                for rot in ctx.get("suggested_rotation", []):
                    st.markdown(f"- {rot}")
        st.info(f"**Justification:** {ctx.get('bleeding_signal_justification', 'N/A')}")

    # --- 4. SALES (VIRTUAL TRY-ON) LOGIC ---
    elif "Sales" in sel_per:
        st.markdown("### Virtual Try-On (VTO) Pipeline")
        if len(files) == 2:
            col1, col2, col3 = st.columns([1, 1, 1.5], gap="large")
            with col1:
                st.markdown("**Source**")
                st.caption(files[0].name)
            with col2:
                st.markdown("**Reference**")
                st.caption(files[1].name)
            with col3:
                st.markdown("**Execution**")
                if st.button("Run Google VTO API", use_container_width=True):
                    with st.spinner("Processing via Google Cloud..."):
                        success = execute_backend_script("scripts/run_virtual_tryon.py", ["--source", files[0].name, "--reference", files[1].name, "--output-dir", "./out"])
                        if success:
                            st.session_state.generated_image = "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&q=80&w=800"
                            st.rerun()
            
            if st.session_state.generated_image:
                st.divider()
                st.markdown("### Synthesized Output")
                st.image(st.session_state.generated_image, use_container_width=True)
        else:
            st.warning("Virtual Try-On requires exactly TWO uploaded images (1 Source Person + 1 Reference Garment).")

    # --- 5. ANALYST LOGIC ---
    elif "Analyst" in sel_per:
        st.markdown("### Bleeding Signal Data Synthesis")
        st.markdown(f"**Summary:** {ctx.get('data_summary', 'N/A')}")
        
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("### Correlated Signals")
            for sig in ctx.get("correlated_bleeding_signals", []):
                st.markdown(f"- {sig}")
        with col2:
            st.markdown("### Missed Opportunities")
            for opp in ctx.get("missed_opportunities", []):
                st.markdown(f"- {opp}")
                
        st.divider()
        if files and files[0].name.endswith('csv'):
            try:
                df = pd.read_csv(files[0])
                st.markdown("### Source DataFrame")
                st.dataframe(df.head(10), use_container_width=True)
                if len(df.columns) >= 2:
                    st.markdown("### Trend Velocity Distribution")
                    st.bar_chart(df.iloc[:, [0, 1]].set_index(df.columns[0]), color="#F5A623")
            except Exception as e:
                st.error("Uploaded file is not a valid CSV or is unreadable.")

    # --- 6. STRATEGY LEADER (Fallback) ---
    else:
        st.markdown("### Executive Synthesis")
        st.json(ctx)
