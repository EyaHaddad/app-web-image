import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
    /* Variables de couleurs */
    :root {
        --primary: #1e3a8a;       /* Dark blue */
        --secondary: #1e40af;     /* Medium blue */
        --accent: #3b82f6;        /* Bright blue */
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --light: #f8fafc;
        --dark: #0f172a;          /* Very dark blue */
        --gray: #64748b;
    }
    
    /* Application principale - Fond bleu foncé */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white !important;
    }
    
    /* Sidebar - Bleu foncé */
    .css-1d391kg, .css-1lcbmhc {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        color: white !important;
    }
    
    /* Contenu de la sidebar */
    .css-1aumxhk {
        background: transparent !important;
        color: white !important;
    }
    
    /* Header - CORRIGÉ */
    .main-header {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        color: white;  
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff 0%, #93c5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 5px solid var(--accent);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        background: rgba(30, 41, 59, 0.95);
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white; 
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Boutons */
    .stButton > button {
        border-radius: 10px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0.75rem 1.5rem;
        width: 100%;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(0, 0, 0, 0.3);
        background: linear-gradient(90deg, var(--secondary) 0%, var(--accent) 100%) !important;
    }
    
    .primary-btn {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
    }
    
    .secondary-btn {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 2px solid var(--accent) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
        color: white !important;
    }
    
    /* Tous les éléments de la sidebar */
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] h5, 
    section[data-testid="stSidebar"] h6 {
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0 2px;
        transition: all 0.3s ease;
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%) !important;
        color: white !important; 
        border-color: var(--accent) !important;
        font-weight: bold;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Sliders */
    .stSlider [data-baseweb="slider"] > div > div {
        background: var(--accent) !important;
    }
    
    .stSlider [data-baseweb="slider"] > div {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
    }
    
    /* Checkboxes et Radio */
    .stCheckbox label, .stRadio label {
        color: white !important;
    }
    
    /* Icons */
    .icon-large {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        color: var(--accent);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 10px;
        background: var(--accent);
        color: white !important;
    }
    
    /* Tooltips */
    .tooltip-icon {
        cursor: help;
        color: var(--accent);
        margin-left: 5px;
    }
    
    /* Split view */
    .split-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        margin: 2rem 0;
    }
    
    .split-line {
        position: absolute;
        width: 4px;
        height: 100%;
        background: var(--accent);
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
        cursor: col-resize;
        border-radius: 2px;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Texte général - TOUT EN BLANC */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    p, span, div {
        color: white !important;
    }
    
    /* Pour les métriques Streamlit */
    [data-testid="stMetric"] {
        color: white !important;
    }
    
    [data-testid="stMetricLabel"], 
    [data-testid="stMetricValue"], 
    [data-testid="stMetricDelta"] {
        color: white !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.8) !important;
        color: white !important;
    }
    
    /* Tables */
    .stDataFrame, .stTable {
        background: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
    }
    
    /* Séparateurs */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Placeholder text */
    ::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.8);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary);
    }
    
    /* Images avec bordure */
    .stImage {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Status messages */
    .stAlert {
        background: rgba(30, 41, 59, 0.9) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: var(--accent) !important;
    }
    
    /* Upload file */
    .stFileUploader {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px dashed var(--accent) !important;
        border-radius: 10px;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
</style>
""", unsafe_allow_html=True)
