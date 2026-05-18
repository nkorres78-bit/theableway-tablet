import streamlit as st
import datetime

# 1. INITIALIZE WEB INTERFACE & DEVICE ENVIRONMENT CONFIG
st.set_page_config(page_title="TheABLEWay - HI-OS Engine Workspace", layout="wide", initial_sidebar_state="expanded")

# 2. SESSION STATE MANAGEMENT & STATE ENGINE INITIALIZATION
if "language" not in st.session_state:
    st.session_state.language = "GR"  # Default fallback language setting
if "current_phase" not in st.session_state:
    st.session_state.current_phase = "Discover"  # Initial system state
if "freeze_count" not in st.session_state:
    st.session_state.freeze_count = 0
if "telemetry_log" not in st.session_state:
    st.session_state.telemetry_log = []

# Workflow State Lock Flags
if "c3_freeze_active" not in st.session_state:
    st.session_state.c3_freeze_active = False
if "c4_freeze_active" not in st.session_state:
    st.session_state.c4_freeze_active = False

# 3. PRODUCTION LOCALIZATION DICTIONARY (EN / GR)
LOCALIZATION = {
    "EN": {
        "app_title": "HI-OS: Human Innovation Operating System",
        "app_subtitle": "TheABLEWay — Cybernetic State Matrix Engine",
        "phase_header": "Active Matrix Row (Phase)",
        "sidebar_header": "Systemic Core Engines",
        "maslow_status": "🔒 Maslow Safety Axis: Active & Validated",
        "maslow_caption": "Biological & physical safety parameters verified. Autonomy gate cleared.",
        "jung_status": "⚖️ Jungian Balance Axis",
        "jung_desc": "Reality Function (Sensing-Thinking) ── Balancing ── Possibilities Function (Intuition-Feeling)",
        "erikson_status": "📈 Psychosocial Transition Axis",
        "erikson_desc": "Identity vs. Role Confusion ➔ Learning to Become",
        "c1_title": "C1: Choose (Defaults) Stance & Parameters",
        "c2_title": "C2: Collect (Mapping) Data Points & Metrics",
        "c3_title": "C3: Connect (Feedback) Mistakes & Risk Assessment",
        "c4_title": "C4: Create (Incentives) Solution / MVP Promise",
        "btn_submit": "Execute State Transition Clearance (submit_solution)",
        "err_c3_freeze": "🚨 WORKFLOW FREEZE (C3 Breach): Empty input detected on C3 (Connect / Mistakes). The negative feedback loop forces mistake analysis to protect your Allostatic Budget from Cultural Drift.",
        "err_c4_freeze": "🚨 WORKFLOW FREEZE (C4 Breach): Empty input detected on C4 (Create / Solution). System locked. Execution state transition clearance withheld until an MVP path or solution string is specified.",
        "success_msg": "Cybernetic verification check passed. Row State transitioned successfully.",
        "telemetry_header": "Cybernetic Operational Telemetry Logs",
        "telemetry_metric": "Total Workflow Freeze Interventions Registered"
    },
    "GR": {
        "app_title": "HI-OS: Human Innovation Operating System",
        "app_subtitle": "TheABLEWay — Κυβερνητική Μηχανή Μήτρας Κατάστασης",
        "phase_header": "Ενεργή Γραμμή Μήτρας (Φάση)",
        "sidebar_header": "Πυρήνες Συστημικής Δομής",
        "maslow_status": "🔒 Άξονας Ασφάλειας Maslow: Ενεργός & Έγκυρος",
        "maslow_caption": "Οι βιολογικές & φυσικές ανάγκες ασφάλειας επαληθεύτηκαν. Έγκριση πύλης αυτονομίας.",
        "jung_status": "⚖️ Άξονας Εξισορρόπησης Jung",
        "jung_desc": "Λειτουργία Πραγματικότητας (Αίσθηση-Σκέψη) ── Αντίβαρο ── Λειτουργία Πιθανοτήτων (Διαίσθηση-Συναίσθημα)",
        "erikson_status": "📈 Άξονας Ψυχοκοινωνικής Μετάβασης",
        "erikson_desc": "Ταυτότητα έναντι Σύγχυσης Ρόλων ➔ Μαθαίνω να Γίνομαι",
        "c1_title": "C1: Choose (Defaults) Στρατηγική & Παράμετροι",
        "c2_title": "C2: Collect (Mapping) Συλλογή Δεδομένων & Μετρικές",
        "c3_title": "C3: Connect (Feedback) Λάθη & Αξιολόγηση Ρίσκου",
        "c4_title": "C4: Create (Incentives) Πρόταση Λύσης / Υπόσχεση MVP",
        "btn_submit": "Εκτέλεση Έγκρισης Μετάβασης Φάσης (submit_solution)",
        "err_c3_freeze": "🚨 WORKFLOW FREEZE (Παραβίαση C3): Εντοπίστηκε κενό πεδίο στο C3 (Connect / Mistakes). Υποχρεωτική ανάλυση σφαλμάτων για προστασία του Allostatic Budget από το Cultural Drift.",
        "err_c4_freeze": "🚨 WORKFLOW FREEZE (Παραβίαση C4): Εντοπίστηκε κενό πεδίο στο C4 (Create / Solution). Το σύστημα κλειδώθηκε. Η έγκριση μετάβασης αναστέλλεται μέχρι να δοθεί μια λύση ή υπόσχεση MVP.",
        "success_msg": "Οι κυβερνητικοί έλεγχοι πέτυχαν. Η κατάσταση της φάσης άλλαξε επιτυχώς.",
        "telemetry_header": "Κυβερνητικά Δεδομένα Τηλεμετρίας & Έλεγχος Συστημάτων",
        "telemetry_metric": "Συνολικές Παρεμβάσεις Workflow Freeze"
    }
}

# Bind localized variables
lang_code = st.session_state.language
tx = LOCALIZATION[lang_code]

# 4. APP INTERFACE LAYOUT & BRANDING HEADERS
st.title(tx["app_title"])
st.subheader(tx["app_subtitle"])

# Language Toggle Switch Bar
col_spacer, col_lang = st.columns([6, 1])
with col_lang:
    ui_lang = st.selectbox("🌐 Language/Γλώσσα", ["GR", "EN"], index=0 if lang_code == "GR" else 1)
    if ui_lang != st.session_state.language:
        st.session_state.language = ui_lang
        st.rerun()

st.divider()

# 5. SIDEBAR COMPONENT: CORE GEOMETRIC AXES VISUALIZER
with st.sidebar:
    st.header(tx["sidebar_header"])
    
    # Axis 1: Maslow Control
    st.success(tx["maslow_status"])
    st.caption(tx["maslow_caption"])
    st.markdown("---")
    
    # Axis 2: Jungian Equilibrium Control
    st.markdown(f"#### {tx['jung_status']}")
    st.info(tx["jung_desc"])
    st.markdown("---")
    
    # Axis 3: Psychosocial Evolution Control
    st.markdown(f"#### {tx['erikson_status']}")
    st.warning(tx["erikson_desc"])

# 6. WORKFLOW MATRIX INTERFACE & PARAMETER COLLECTION GRID
st.header(f"📍 {tx['phase_header']}: `{st.session_state.current_phase.upper()}`")

# Informative nodes map tracking active EntreComp profiles
phase_mapping_directory = {
    "Discover": "#1 Coping with VUCA, #2 Ethical Thinking, #14 Mistakes Assessment, #13 Enjoy Creativity",
    "Define": "#7 Purpose & Direction, #5 Mobilizing Resources, #6 Learning to Become, #15 Proposal MVP",
    "Develop": "#3 Spotting Opportunities, #4 Planning & Management, #8 Working with Others, #12 Learning to Co-create",
    "Deliver": "#9 Taking the Initiative, #10 Managing Performance, #11 Views / Perspectives, #16 Product / Service"
}
st.caption(f"**EntreComp Profile Alignment:** {phase_mapping_directory[st.session_state.current_phase]}")

# Matrix Formulation Form
with st.form(key="hi_os_matrix_form"):
    c1_data = st.text_input(tx["c1_title"])
    c2_data = st.text_area(tx["c2_title"])
    c3_data = st.text_area(tx["c3_title"])
    c4_data = st.text_area(tx["c4_title"])
    
    # "submit_solution" trigger mechanism button
    submit_solution = st.form_submit_button(label=tx["btn_submit"])

# 7. CYBERNETIC VALIDATION PATH & DOUBLE CRITICAL CONSTRAINT LOOP
if submit_solution:
    # Clear visual state flags from previous loop cycles
    st.session_state.c3_freeze_active = False
    st.session_state.c4_freeze_active = False

    # Stance Check 1: Operational C3 Empty Constraint Verification
    if not c3_data.strip():
        st.session_state.c3_freeze_active = True
        st.session_state.freeze_count += 1
        
    # Stance Check 2: Identical C4 Empty Constraint Verification
    if not c4_data.strip():
        st.session_state.c4_freeze_active = True
        st.session_state.freeze_count += 1

    # Logic Evaluator: If any condition broke, store event telemetry payload
    if st.session_state.c3_freeze_active or st.session_state.c4_freeze_active:
        telemetry_payload = {
            "timestamp": str(datetime.datetime.now()),
            "system_state_phase": st.session_state.current_phase,
            "execution_status": "WORKFLOW_FREEZE_TRIGGERED",
            "c3_breached": st.session_state.c3_freeze_active,
            "c4_breached": st.session_state.c4_freeze_active,
            "accumulated_freeze_telemetry": st.session_state.freeze_count
        }
        st.session_state.telemetry_log.append(telemetry_payload)
    else:
        # Clearance Granted: Progress sequentially through Design Thinking 4Ds Matrix Axis
        state_transition_map = {
            "Discover": "Define",
            "Define": "Develop",
            "Develop": "Deliver",
            "Deliver": "Discover"
        }
        previous_phase = st.session_state.current_phase
        st.session_state.current_phase = state_transition_map[previous_phase]
        
        # Log successful operational clearance metadata packet
        telemetry_payload = {
            "timestamp": str(datetime.datetime.now()),
            "execution_status": "STATE_TRANSITION_CLEARANCE_GRANTED",
            "transition_vector": f"{previous_phase} ➔ {st.session_state.current_phase}",
            "accumulated_freeze_telemetry": st.session_state.freeze_count
        }
        st.session_state.telemetry_log.append(telemetry_payload)
        st.toast(tx["success_msg"], icon="✅")
        st.rerun()

# 8. CONDITIONAL WORKFLOW INTERVENTION ERROR RENDERING
if st.session_state.c3_freeze_active:
    st.error(tx["err_c3_freeze"])

if st.session_state.c4_freeze_active:
    st.error(tx["err_c4_freeze"])

# 9. PERFORMANCE TELEMETRY AUDIT TRAIL DATA STREAM
st.divider()
st.subheader(tx["telemetry_header"])

col_metric, _ = st.columns([2, 5])
with col_metric:
    st.metric(label=tx["telemetry_metric"], value=st.session_state.freeze_count, delta=None)

if st.session_state.telemetry_log:
    with st.expander("View Payload Stream (JSON Ledger)", expanded=False):
        st.json(st.session_state.telemetry_log)
