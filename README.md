Tiger Analytics | Sense & Respond OS

Bleeding Signals Engine — Multimodal Agentic Operating System
Powered by Groq (llama-3.3-70b-versatile) · SMART Signal Framework · 5-Persona Routing


Quick Start
bashpip install -r requirements.txt
export GROQ_API_KEY=gsk_...          # or enter in-app
streamlit run app.py
Place tiger_logo.png in the same directory as app.py for the branded logo.

Architecture (mirrors n8n backend)
Context Resolution  (00_Config_Registry equivalent)
        ↓
Source Ingestion    (uploaded file / CSV / image / text)
        ↓
Synthesis Agent     (Groq LLM — SMART Bleeding Signal JSON)
        ↓
Score Acceleration  (deterministic: specificity + social + blog bonus)
+ Saturation        (arbitrage_index = virality×0.4 + accel×0.4 + sat_bonus×0.2)
        ↓
Persona Router      (Switch on branch)
   ├── Brand Manager      → commercial_with_review   → Orch + Reflect
   ├── Demand Planner     → execution_with_review    → Orch + Reflect
   ├── Data Scientist     → evidence_artifact        → Orch only
   ├── Data Engineer      → technical_artifact       → Orch only
   └── Compliance Officer → risk_review_only         → Reflect only
        ↓
Orchestration Agent (persona-specific artifact)
        ↓
Reflection Agent    (governance + brand safety — review branches only)
        ↓
Generative Studio   (Signal Alert Cards · Persona Output · JSON Export)

SMART Bleeding Signal Framework
Every signal the Synthesis Agent returns is validated against:
DimensionRequirementSpecificHyper-niche keyword (e.g. "gorpcore utility vest", not "outdoor fashion")Measurablebleeding_edge_virality_score (1–100) + velocity_metricActionableDirectly usable as Imagen 3 / ad creative promptRelevant & Time-boundGrounded in uploaded context + emergence_window
Signals with bleeding_edge_virality_score ≥ 85 trigger Extreme Virality mode with a mandatory extreme_action_directive.

Scoring Model
MetricFormulaacceleration_scorevirality × 0.6 + specificity_bonus + social_bonus + blog_bonus (capped 100)saturation_riskHIGH (≥85) / MEDIUM (≥60) / LOW (<60)arbitrage_indexvirality×0.4 + acceleration×0.4 + saturation_bonus×0.2

Backend Script Integration
Place these in your project root and they're invoked via subprocess:
ScriptCLI ArgsTriggerscripts/generate_trend_image.py--influencer-id --trend-idImagen 3 button in Signals tabscripts/run_virtual_tryon.py--source --reference --output-dirVTO button in Signals tab

Environment Variables
VariablePurposeGROQ_API_KEYGroq API key (or enter in-app sidebar)

File Upload Support
TypeUsed for.csvSocial listening exports, trend data, sales data.txtNews digests, editorial summaries, Reddit threads.png/.jpg/.jpegVisual trend references (processed as context label)
