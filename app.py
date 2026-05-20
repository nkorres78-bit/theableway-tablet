import streamlit as st
import time
import pandas as pd
from datetime import datetime
import requests

# ==============================================================================
# 1. INITIAL SYSTEM CONFIGURATION & UI SETUP
# ==============================================================================
st.set_page_config(
    page_title="TheABLEWay System",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for production-grade visual anchors and heavy-duty active friction
st.markdown("""
<style>
    .reportview-container .main .block-container { max-width: 600px; padding-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5rem; font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem; }
    div[data-baseweb="textarea"] { border-radius: 12px; }
    .freeze-box { background-color: #ffe6e6; border: 3px solid #ff4d4d; padding: 1.5rem; border-radius: 16px; color: #cc0000; font-weight: bold; margin-bottom: 1.5rem; text-align: center; }
    .success-box { background-color: #e6f9ec; border: 3px solid #2db359; padding: 1.5rem; border-radius: 16px; color: #1a6633; font-weight: bold; margin-bottom: 1.5rem; text-align: center; }
    .action-card { background-color: #f7f9fa; border-left: 6px solid #ff9900; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

# Initialize programmatic telemetry and state tracking arrays
if 'step' not in st.session_state: st.session_state.step = 'LANG_SELECTION'
if 'lang' not in st.session_state: st.session_state.lang = 'GR'
if 'category' not in st.session_state: st.session_state.category = None
if 'sub_step' not in st.session_state: st.session_state.sub_step = 'INPUT_PHASE'

# Telemetry data storage metrics
if 't_start' not in st.session_state: st.session_state.t_start = time.time()
if 'freeze_count' not in st.session_state: st.session_state.freeze_count = 0
if 'c1_input' not in st.session_state: st.session_state.c1_input = ""
if 'c2_tag' not in st.session_state: st.session_state.c2_tag = ""
if 'c2_text' not in st.session_state: st.session_state.c2_text = ""
if 'c3_tag' not in st.session_state: st.session_state.c3_tag = ""
if 'c3_text' not in st.session_state: st.session_state.c3_text = ""
if 'c4_tag' not in st.session_state: st.session_state.c4_tag = ""
if 'c4_text' not in st.session_state: st.session_state.c4_text = ""

# Google Sheets Dedicated URL Configuration
WEBAPP_URL = "https://google.com"

# ==============================================================================
# 2. LOCALIZED SEMANTIC DICTIONARIES (LEXICON SCALABILITY)
# ==============================================================================
LEXICON = {
    'GR': {
        'welcome': "🧩 TheABLEWay System",
        'sub': "Γνωστική Σκαλωσιά Διαχείρισης Άγχους",
        'q_cat': "Πού εντοπίζεται το ζόρι σήμερα;",
        'cat_love': "❤️ Σχέσεις & Ερωτικά",
        'cat_fam': "👪 Οικογένεια & Φίλοι",
        'cat_money': "💸 Δουλειά & Οικονομικά",
        'freeze_c3': "⚠️ WORKFLOW FREEZE! Δεν μπορείς να πας στη λύση αν δεν κοιτάξεις πρώτα το λάθος σου. Συμπλήρωσε το πεδίο.",
        'freeze_c4': "⚠️ WORKFLOW FREEZE! Δεν μπορείς να ολοκληρώσεις τη διαδρομή αν δεν δεσμευτείς σε μια συγκεκριμένη λύση. Συμπλήρωσε το πεδίο.",
        'submit_analysis': "Ανάλυση Λάθους ➔",
        'submit_solution': "Δημιουργία Action Plan ✔️",
        'survey_q': "Βοήθησε αυτή η διαδρομή να μειωθεί το άγχος σου;",
        'survey_1': "Καθόλου", 'survey_2': "Λίγο", 'survey_3': "Αρκετά", 'survey_4': "Πολύ",
        'final_thanks': "💯 Μπράβο! Η γνωστική σου σκαλωσιά ολοκληρώθηκε. Μόλις άλλαξες τον τρόπο που σκέφτεσαι.",
        'restart': "Νέα Διαδρομή",
        'c1_q_biz': "Ποιος άνθρωπος ή ρόλος βρίσκεται στο επίκεντρο του προβλήματος;",
        'c1_q_love': "Ποιος άνθρωπος εμπλέκεται στην κατάσταση αυτή τη στιγμή;",
        'c2_q_general': "Ποιος είναι ο κύριος άξονας της ανάγκης σου αυτή τη στιγμή;",
        'c2_text_prompt': "Εξήγησε σε 1-2 προτάσεις τι ακριβώς σου λείπει:",
        'c3_q_general': "Πού εντοπίζεται το δικό σου σφάλμα ή η παράλειψη;",
        'c3_text_prompt': "Γράψε με ειλικρίνεια τι ακριβώς έκανες λάθος:",
        'c4_q_general': "Ποιος είναι ο τύπος της άμεσης παρέμβασης που θα επιλέξεις;",
        'c4_text_prompt': "Περίγραψε την ακριβή, μικρή πράξη που θα εκτελέσεις μόλις κατεβείς:",
        'opt_empty': "[Επίλεξε...]",
        'opt_me': "Εγώ ο ίδιος",
        'opt_team': "Συνεργάτης / Ομάδα",
        'opt_mgmt': "Διοίκηση / Αφεντικό",
        'opt_ext': "Εξωτερικός / Τρίτος",
        'opt_partner': "Σύντροφος / Σύζυγος",
        'opt_ex': "Πρώην",
        'opt_crush': "Πρόσωπο που με ενδιαφέρει",
        'opt_family': "Γονέας / Παιδί / Συγγενής",
        'opt_friend': "Φίλος / Κολλητός",
        'ap_title': "📝 Το Προσωπικό σου Action Plan",
        'ap_context': "• Η Κατάσταση (Ποιος):",
        'ap_need': "• Η Ανάγκη σου (Τι):",
        'ap_mistake': "• Το Σφάλμα (Γιατί):",
        'ap_action': "• Η Δέσμευσή σου (Πώς):",
        
        # PATH A: PERSONAL/RELATIONAL LABELS (LOVE, FAMILY)
        'p_c2_1': "🎭 Ταυτότητα (Να με υπολογίζουν / Να με ακούν)",
        'p_c2_2': "📊 Πόροι (Ξέμεινα από δυνάμεις / Χρειάζομαι ησυχία)",
        'p_c2_3': "🗣️ Επικοινωνία (Να βρούμε μια κοινή γραμμή / Να συνεννοηθούμε)",
        'p_c2_4': "🎯 Πράξη (Να βρεθεί μια λύση τώρα / Να δω αποτέλεσμα)",
        
        'p_c3_1': "🎭 Ταυτότητα (Κοίταξα μόνο το δικό μου εγώ / την περηφάνια μου)",
        'p_c3_2': "📊 Πόροι (Το παράκανα / Πίεσα υπερβολικά τις αντοχές μου)",
        'p_c3_3': "🗣️ Επικοινωνία (Μίλησα σε λάθος στιγμή ή με λάθος τόνο)",
        'p_c3_4': "🎯 Πράξη (Παρεξήγηση / Υπέθεσα πράγματα χωρίς να ξέρω)",
        
        'p_c4_1': "🎭 Ταυτότητα (Θα αλλάξω στάση / Θα κάνω πίσω)",
        'p_c4_2': "📊 Πόροι (Βάζω ένα stop / Προστατεύω τον εαυτό μου)",
        'p_c4_3': "🗣️ Επικοινωνία (Θα στείλω ένα καθαρό μήνυμα / Θα κάνω μια ευθεία κουβέντα)",
        'p_c4_4': "🎯 Πράξη (Θα κάνω μια συγκεκριμένη, μικρή πράξη)",

        # PATH B: MATERIAL/WORK LABELS (MONEY)
        'm_c2_1': "🎭 Ταυτότητα (Να σεβαστούν τον επαγγελματικό μου ρόλο / τη θέση μου)",
        'm_c2_2': "📊 Πόροι (Χρειάζομαι οικονομική ασφάλεια / Ξέμεινα από χρόνο)",
        'm_c2_3': "🗣️ Επικοινωνία (Να ξεκαθαρίσουν οι όροι / Να ευθυγραμμιστούμε)",
        'm_c2_4': "🎯 Πράξη (Να κλείσει το θέμα άμεσα / Να δω έργο)",
        
        'm_c3_1': "🎭 Ταυτότητα (Το πήρα προσωπικά / Επέβαλα τη δική μου αυθεντία)",
        'm_c3_2': "📊 Πόροι (Το παράκανα με τα έξοδα / Υπολόγισα λάθος τα deadlines)",
        'm_c3_3': "🗣️ Επικοινωνία (Χρησιμοποίησα λάθος κανάλι / Μίλησα σε λάθος timing)",
        'm_c3_4': "🎯 Πράξη (Βασίστηκα σε αυθαίρετες προβλέψεις / Έκανα τυφλές υποθέσεις)",
        
        'm_c4_1': "🎭 Ταυτότητα (Θα αλλάξω επαγγελματική στάση / Θα υποχωρήσω)",
        'm_c4_2': "📊 Πόροι (Παγώνω τα έξοδα / Ζητάω παράταση χρόνου)",
        'm_c4_3': "🗣️ Επικοινωνία (Ζητάω επίσημη διευκρίνιση / Στέλνω γραπτό feedback)",
        'm_c4_4': "🎯 Πράξη (Θα εκτελέσω ένα συγκεκριμένο επόμενο task)"
    },
    'EN': {
        'welcome': "🧩 TheABLEWay System",
        'sub': "Cognitive Scaffolding Framework",
        'q_cat': "Where is the friction originating today?",
        'cat_love': "❤️ Relationships & Love",
        'cat_fam': "👪 Family & Friends",
        'cat_money': "💸 Work & Finances",
        'freeze_c3': "⚠️ WORKFLOW FREEZE! You cannot bypass failure analysis. Analyze your error to unlock execution.",
        'freeze_c4': "⚠️ WORKFLOW FREEZE! You cannot complete execution without defining an action plan. Secure the solution vector.",
        'submit_analysis': "Analyze Error ➔",
        'submit_solution': "Generate Action Plan ✔️",
        'survey_q': "Did this structured trajectory reduce your situational anxiety?",
        'survey_1': "Not at all", 'survey_2': "Slightly", 'survey_3': "Significantly", 'survey_4': "Completely",
        'final_thanks': "💯 Execution Verified! Your cognitive scaffolding is complete. Prediction patterns updated.",
        'restart': "Restart System",
        'c1_q_biz': "Which individual or role is at the core of this block?",
        'c1_q_love': "Who is the other individual involved in this friction right now?",
        'c2_q_general': "What is the primary axis of your resource deficiency right now?",
        'c2_text_prompt': "Explain what you accurately lack in 1-2 sentences:",
        'c3_q_general': "Where is your operational error or strategic oversight located?",
        'c3_text_prompt': "Write with absolute sincerity what exactly you executed wrong:",
        'c4_q_general': "What type of immediate low-risk nudge will you deploy?",
        'c4_text_prompt': "Describe the exact micro-action you will execute upon exit:",
        'opt_empty': "[Select...]",
        'opt_me': "Myself",
        'opt_team': "Team Member / Peer",
        'opt_mgmt': "Management / Boss",
        'opt_ext': "External / Third Party",
        'opt_partner': "Partner / Spouse",
        'opt_ex': "Ex-partner",
        'opt_crush': "Someone I am interested in",
        'opt_family': "Parent / Child / Relative",
        'opt_friend': "Friend / Close Peer",
        'ap_title': "📝 Your Personal Action Plan",
        'ap_context': "• Target Node (Who):",
        'ap_need': "• Systemic Need (What):",
        'ap_mistake': "• Connection Failure (Why):",
        'ap_action': "• Active Commitment (How):",
        
        'p_c2_1': "🎭 Identity (To be valued / To be heard)",
        'p_c2_2': "📊 Resources (Burned out / Need peace and quiet)",
        'p_c2_3': "🗣️ Communication (Find a common alignment / Synchronize)",
        'p_c2_4': "🎯 Action (Need a resolution now / See actual results)",
        
        'p_c3_1': "🎭 Identity (Focused purely on my own ego / pride)",
        'p_c3_2': "📊 Resources (Overdid it / Pushed my limits too hard)",
        'p_c3_3': "🗣️ Communication (Spoke at the wrong moment or wrong tone)",
        'p_c3_4': "🎯 Action (Misunderstanding / Made blind assumptions)",
        
        'p_c4_1': "🎭 Identity (I will change my posture / Step back)",
        'p_c4_2': "📊 Resources (Set an absolute stop / Protect my limits)",
        'p_c4_3': "🗣️ Communication (Send a clear text / Direct synchronous talk)",
        'p_c4_4': "🎯 Action (Execute a single explicit micro-action)",

        'm_c2_1': "🎭 Identity (To respect my professional role / my position)",
        'm_c2_2': "📊 Resources (Need financial security / Out of budget or time)",
        'm_c2_3': "🗣️ Communication (Clarify terms / Align goals)",
        'm_c2_4': "🎯 Action (Resolve the topic immediately / See production output)",
        
        'm_c3_1': "🎭 Identity (Took it personally / Imposed my own authority)",
        'm_c3_2': "📊 Resources (Overspent funds / Miscalculated deadlines)",
        'm_c3_3': "🗣️ Communication (Used wrong channel / Spoke at wrong timing)",
        'm_c3_4': "🎯 Action (Relied on blind forecasts / Made assumptions without data)",
        
        'm_c4_1': "🎭 Identity (Change professional stance / Back down)",
        'm_c4_2': "📊 Resources (Freeze expenditures / Request time extension)",
        'm_c4_3': "🗣️ Communication (Request formal clarification / Send written feedback)",
        'm_c4_4': "🎯 Action (Execute a single specific next task)"
    }
}

def txt(key):
    return LEXICON[st.session_state.lang][key]

def push_telemetry_to_sheets(payload):
    try:
        requests.post(WEBAPP_URL, data=payload, timeout=5)
    except Exception:
        pass

# ==============================================================================
# 3. INTERACTIVE DETERMINISTIC STATE MACHINE FLOWS
# ==============================================================================

# STAGE A: Language Selection UI Layout
if st.session_state.step == 'LANG_SELECTION':
    st.title("🧩 TheABLEWay")
    st.subheader("Select Language / Επιλογή Γλώσσας")
    col1, col2 = st.columns(2)
    if col1.button("ΕΛΛΗΝΙΚΑ 🇬🇷"):
        st.session_state.lang = 'GR'; st.session_state.step = 'CATEGORY_SELECTION'; st.rerun()
    if col2.button("ENGLISH 🇺🇸"):
        st.session_state.lang = 'EN'; st.session_state.step = 'CATEGORY_SELECTION'; st.rerun()

# STAGE B: Direct Clean 3-Node Context Gate Layout
elif st.session_state.step == 'CATEGORY_SELECTION':
    st.title(txt('welcome'))
    st.subheader(txt('q_cat'))
    if st.button(txt('cat_love')): st.session_state.category = 'LOVE'; st.session_state.step = 'MATRIX_LOOP'; st.rerun()
    if st.button(txt('cat_fam')): st.session_state.category = 'FAMILY'; st.session_state.step = 'MATRIX_LOOP'; st.rerun()
    if st.button(txt('cat_money')): st.session_state.category = 'MONEY'; st.session_state.step = 'MATRIX_LOOP'; st.rerun()

# STAGE C: Production Execution Matrix Layer (The Cs Matrix Layout)
elif st.session_state.step == 'MATRIX_LOOP':
    st.title(txt('welcome'))
    
    # Assign options and semantic mappings based on selected Context Node
    if st.session_state.category == 'LOVE':
        options_list = [txt('opt_empty'), txt('opt_me'), txt('opt_partner'), txt('opt_ex'), txt('opt_crush')]
        q1 = txt('c1_q_love')
        c2_choices = [txt('p_c2_1'), txt('p_c2_2'), txt('p_c2_3'), txt('p_c2_4')]
        c3_choices = [txt('p_c3_1'), txt('p_c3_2'), txt('p_c3_3'), txt('p_c3_4')]
    elif st.session_state.category == 'FAMILY':
        options_list = [txt('opt_empty'), txt('opt_me'), txt('opt_family'), txt('opt_friend')]
        q1 = txt('c1_q_love')
        c2_choices = [txt('p_c2_1'), txt('p_c2_2'), txt('p_c2_3'), txt('p_c2_4')]
        c3_choices = [txt('p_c3_1'), txt('p_c3_2'), txt('p_c3_3'), txt('p_c3_4')]
    else:  # MONEY Path
        options_list = [txt('opt_empty'), txt('opt_me'), txt('opt_team'), txt('opt_mgmt'), txt('opt_ext')]
        q1 = txt('c1_q_biz')
        c2_choices = [txt('m_c2_1'), txt('m_c2_2'), txt('m_c2_3'), txt('m_c2_4')]
        c3_choices = [txt('m_c3_1'), txt('m_c3_2'), txt('m_c3_3'), txt('m_c3_4')]

    # STEP C1: Input Validation Phase (C1, C2, C3)
    if st.session_state.sub_step == 'INPUT_PHASE':
        st.session_state.c1_input = st.selectbox(q1, options_list)
        
        if st.session_state.c1_input != txt('opt_empty'):
            st.write("---")
            st.subheader(txt('c2_q_general'))
            st.session_state.c2_tag = st.radio("Select Axis:", c2_choices, key="c2_radio")
            st.session_state.c2_text = st.text_area(txt('c2_text_prompt'), value=st.session_state.c2_text, key="c2_area")
            
        if st.session_state.c1_input != txt('opt_empty') and st.session_state.c2_text.strip() != "":
            st.write("---")
            st.subheader(txt('c3_q_general'))
            st.session_state.c3_tag = st.radio("Select Axis:", c3_choices, key="c3_radio")
            st.session_state.c3_text = st.text_area(txt('c3_text_prompt'), value=st.session_state.c3_text, key="c3_area")
            
        if st.session_state.c1_input != txt('opt_empty') and st.session_state.c2_text.strip() != "":
            if st.button(txt('submit_analysis')):
                if "c2_area" in st.session_state: st.session_state.c2_text = st.session_state.c2_area
                if "c3_area" in st.session_state: st.session_state.c3_text = st.session_state.c3_area
                
                # Active Friction Enforcement Check 1 (C3 Freeze)
                if st.session_state.c3_text.strip() == "":
                    st.session_state.freeze_count += 1
                    st.markdown(f'<div class="freeze-box">{txt("freeze_c3")}</div>', unsafe_allow_html=True)
                else:
                    st.session_state.sub_step = 'SOLUTION_PHASE'
                    st.rerun()

    # STEP C2: Solution Generation Isolated Phase (C4 only with 2nd Freeze Engine)
    elif st.session_state.sub_step == 'SOLUTION_PHASE':
        st.markdown(f"**{txt('c3_q_general')}**\n\n*{st.session_state.c3_text}*")
        st.write("---")
        
        # Load C4 dynamic labels path mapping
        c4_choices = [txt('p_c4_1'), txt('p_c4_2'), txt('p_c4_3'), txt('p_c4_4')] if st.session_state.category in ['LOVE', 'FAMILY'] else [txt('m_c4_1'), txt('m_c4_2'), txt('m_c4_3'), txt('m_c4_4')]
        
        st.subheader(txt('c4_q_general'))
        st.session_state.c4_tag = st.radio("Select Axis:", c4_choices, key="c4_radio")
        st.session_state.c4_text = st.text_area(txt('c4_text_prompt'), value=st.session_state.c4_text, key="c4_area")
        
        if st.button(txt('submit_solution')):
            if "c4_area" in st.session_state: st.session_state.c4_text = st.session_state.c4_area
            
            # Active Friction Enforcement Check 2 (C4 Freeze)
            if st.session_state.c4_text.strip() == "":
                st.session_state.freeze_count += 1
                st.markdown(f'<div class="freeze-box">{txt("freeze_c4")}</div>', unsafe_allow_html=True)
            else:
                st.session_state.step = 'ACTION_PLAN_DISPLAY'
                st.rerun()

# STAGE D: Unified Mirror Feedback Output & Anxiety Survey Layer
elif st.session_state.step == 'ACTION_PLAN_DISPLAY':
    st.title(txt('welcome'))
    
    # Extract structural tags safely
    c2_axis_code = st.session_state.c2_tag if st.session_state.c2_tag else "🌀"
    c3_axis_code = st.session_state.c3_tag if st.session_state.c3_tag else "🌀"
    c4_axis_code = st.session_state.c4_tag if st.session_state.c4_tag else "🌀"
    
    # Render the Mirror Card firmly at the top of the interface
    st.markdown(f"""
    <div class="action-card">
        <h3>{txt('ap_title')}</h3>
        <p><b>{txt('ap_context')}</b> {st.session_state.c1_input}</p>
        <p><b>{txt('ap_need')}</b> {c2_axis_code}</p>
        <p style="padding-left: 15px; font-style: italic; color: #555;">"{st.session_state.c2_text}"</p>
        <p><b>{txt('ap_mistake')}</b> {c3_axis_code}</p>
        <p style="padding-left: 15px; font-style: italic; color: #555;">"{st.session_state.c3_text}"</p>
        <p><b>{txt('ap_action')}</b> <span style='color:#ff9900; font-size:1.1rem;'><b>{c4_axis_code}</b></span></p>
        <p style="padding-left: 15px; font-style: italic; color: #ff9900; font-weight: bold;">"{st.session_state.c4_text}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader(txt('survey_q'))
    
    col1, col2, col3, col4 = st.columns(4)
    score = 0
    if col1.button(txt('survey_1')): score = 1
    if col2.button(txt('survey_2')): score = 2
    if col3.button(txt('survey_3')): score = 3
    if col4.button(txt('survey_4')): score = 4
    
    if score > 0:
        # Compute exact execution time frame metrics
        t_end = time.time()
        elapsed_seconds = round(t_end - st.session_state.t_start, 2)
        
        # FIXED COUPLING KEY: Force payload mapping back to the public parameter names
        telemetry_payload = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Language": st.session_state.lang,
            "Duration_Profile": "ADAPTIVE",
            "Context_Archetype": st.session_state.category,
            "Category_Node": st.session_state.category,
            "Total_Execution_Time_Sec": elapsed_seconds,
            "Friction_Freeze_Events": st.session_state.freeze_count,
            "Anxiety_Reduction_Score": score,
            "C1_Choose_Data": st.session_state.c1_input,
            "To_Vector_Selected": st.session_state.c2_tag[:15], # Hard match to what Google Apps Script expects
            "C2_Collect_Data": st.session_state.c2_text.replace("\n", " "),
            "C3_Vector_Selected": st.session_state.c3_tag[:15],
            "C3_Connect_Mistake_Data": st.session_state.c3_text.replace("\n", " "),
            "C4_Vector_Selected": st.session_state.c4_tag[:15],
            "C4_Create_Solution_Data": st.session_state.c4_text.replace("\n", " ")
        }
        
        # Execute direct data append push
        push_telemetry_to_sheets(telemetry_payload)
        
        st.session_state.step = 'COMPLETE'
        st.rerun()

# STAGE E: Terminal Clean Layout (No Log Visible)
elif st.session_state.step == 'COMPLETE':
    st.markdown(f'<div class="success-box">{txt("final_thanks")}</div>', unsafe_allow_html=True)
    
    if st.button(txt('restart')):
        # Clear localized runtime stacks entirely to reboot the loop safely
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.session_state.step = 'LANG_SELECTION'
        st.session_state.sub_step = 'INPUT_PHASE'
        st.rerun()
