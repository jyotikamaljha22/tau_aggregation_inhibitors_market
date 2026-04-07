import os
import csv
from datetime import datetime, timezone
import streamlit as st
import streamlit.components.v1 as components

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="CantaBio Strategic Report",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# CSS HIDING (WHITE-LABELING)
# ----------------------------
st.markdown(
    """
    <style>
    /* Hide Streamlit UI elements for a pure app feel */
    [data-testid="stToolbar"] { display: none !important; }
    .viewerBadge_container, #viewerBadge_container { display: none !important; }
    footer { display: none !important; }
    header[data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
    
    /* Make the Streamlit sidebar match the Slate theme of the HTML */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    /* Form input styling */
    .stTextInput input {
        border-radius: 8px !important;
    }
    .stButton > button {
        background-color: #0F766E !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #115E59 !important;
    }
    
    /* Viewer Chip */
    .viewer-chip {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        background: #E2E8F0;
        color: #0F172A;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# LOGGING (WHO ACCESSED)
# ----------------------------
def log_access(name, email):
    log_file = "cantabio_access_log.csv"
    record = {
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "viewer_name": name.strip(),
        "viewer_email": email.strip()
    }
    try:
        write_header = not os.path.exists(log_file)
        with open(log_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp_utc", "viewer_name", "viewer_email"])
            if write_header:
                writer.writeheader()
            writer.writerow(record)
    except Exception:
        pass

# ----------------------------
# ACCESS CONTROL
# ----------------------------
def check_access():
    expected_password = str(st.secrets.get("ACCESS_CODE", "SMR2026")).strip()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    with st.sidebar:
        st.markdown("<h3 style='color:#0F172A; font-weight:800; font-family:sans-serif;'>🔐 Secure Login</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748B; font-size:0.85rem; margin-bottom:1rem;'>CantaBio Boardroom Advisory</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            name = st.text_input("Name*")
            email = st.text_input("Email*")
            password = st.text_input("Access Code*", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            enter = st.form_submit_button("Enter Dashboard", use_container_width=True)

    if enter:
        clean_name = name.strip()
        clean_email = email.strip()
        clean_pass = password.strip()
        
        if not clean_name or not clean_email or not clean_pass:
            st.sidebar.warning("⚠️ Please fill in all fields.")
        elif clean_pass != expected_password:
            st.sidebar.error("❌ Invalid Access Code.")
        else:
            st.session_state.authenticated = True
            st.session_state.viewer_name = clean_name
            log_access(clean_name, clean_email)
            st.rerun()

    if not st.session_state.authenticated:
        st.markdown(
            """
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:60vh; font-family:sans-serif;">
                <h2 style='color:#0F172A; font-weight:800; font-size:2.4rem;'>Dashboard Secured</h2>
                <p style='color:#64748B; font-size:1.1rem;'>Please use the sidebar to authenticate and load the strategic report.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.stop()

    return True

# ----------------------------
# MAIN APP EXECUTION
# ----------------------------
check_access()

# Authenticated Sidebar
viewer_name = st.session_state.get("viewer_name", "Guest")
st.sidebar.markdown(f'<div class="viewer-chip">Verified: {viewer_name}</div>', unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:0.85rem; color:#64748B;'>Use the navigation menu inside the dashboard to jump between sections.</p>", unsafe_allow_html=True)

st.sidebar.markdown("---")
if st.sidebar.button("End Session", use_container_width=True):
    st.session_state.authenticated = False
    st.rerun()

# ----------------------------
# HTML DASHBOARD CONTENT
# ----------------------------
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Tau Aggregation Inhibitors Market (2025–2035) | CantaBio</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #F8FAFC; 
            color: #0F172A; 
        }
        
        .consulting-table th {
            border-bottom: 2px solid #334155;
            padding: 12px 8px;
            text-align: right;
            font-size: 0.875rem;
            font-weight: 600;
            color: #1E293B;
        }
        
        .consulting-table th:first-child {
            text-align: left;
        }
        
        .consulting-table td {
            border-bottom: 1px solid #E2E8F0;
            padding: 10px 8px;
            text-align: right;
            font-size: 0.875rem;
            color: #475569;
        }
        
        .consulting-table td:first-child {
            text-align: left;
            font-weight: 500;
            color: #0F172A;
        }

        .consulting-table tr:hover td {
            background-color: #F1F5F9;
        }

        .chart-container {
            position: relative;
            width: 100%;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            height: 350px;
            max-height: 400px;
            padding: 1rem;
            background-color: #ffffff;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            border: 1px solid #E2E8F0;
        }

        @media (max-width: 768px) {
            .chart-container {
                height: 250px;
                max-width: 100%;
            }
        }
        
        .sidebar {
            height: 100vh;
            position: sticky;
            top: 0;
        }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #f1f1f1; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    </style>
</head>
<body class="flex flex-col md:flex-row min-h-screen">

    <div class="md:hidden bg-slate-900 text-white p-4 flex justify-between items-center sticky top-0 z-50">
        <div class="font-bold text-lg">CantaBio Strategic Report</div>
        <button id="mobile-menu-btn" class="text-2xl focus:outline-none">&#9776;</button>
    </div>

    <nav id="sidebar" class="sidebar hidden md:flex flex-col w-full md:w-64 bg-slate-900 text-slate-300 transition-all duration-300 z-40">
        <div class="p-6">
            <h1 class="text-white font-bold text-xl leading-tight mb-2">Tau Aggregation Market</h1>
            <p class="text-xs text-slate-400 font-medium tracking-wider uppercase mb-8">2025–2035 Strategy</p>
            
            <ul class="space-y-2 text-sm font-medium">
                <li><a href="#exec-summary" class="nav-link block py-2 px-3 rounded hover:bg-slate-800 hover:text-white transition active-nav">Executive Summary</a></li>
                <li><a href="#market-transition" class="nav-link block py-2 px-3 rounded hover:bg-slate-800 hover:text-white transition">1. SoC to Tau Transition</a></li>
                <li><a href="#patient-funnel" class="nav-link block py-2 px-3 rounded hover:bg-slate-800 hover:text-white transition">2. Patient Funnel Logic</a></li>
                <li><a href="#competitive-dynamics" class="nav-link block py-2 px-3 rounded hover:bg-slate-800 hover:text-white transition">3. Competitive Dynamics</a></li>
                <li><a href="#cantabio-strategy" class="nav-link block py-2 px-3 rounded hover:bg-slate-800 hover:text-white transition">4. CantaBio Strategic Positioning</a></li>
            </ul>
        </div>
        <div class="mt-auto p-6 border-t border-slate-800 text-xs text-slate-500">
            Prepared for CantaBio Board of Directors<br>
            April 2026
        </div>
    </nav>

    <main class="flex-1 w-full bg-slate-50 p-4 md:p-8 overflow-y-auto">
        
        <div class="max-w-5xl mx-auto space-y-12">
            
            <header class="mb-12 border-b-2 border-teal-700 pb-6">
                <div class="flex items-center text-teal-700 mb-4">
                    <span class="text-2xl mr-2">&#9632;</span>
                    <span class="font-bold tracking-widest uppercase text-sm">Boardroom Strategic Advisory Document</span>
                </div>
                <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 mb-4 leading-tight">Global Tau Aggregation Inhibitors Market (2025–2035)</h1>
                <h2 class="text-xl md:text-2xl text-slate-600 font-light leading-relaxed">Transition from Standard of Care to Tau-Targeted Therapies & Strategic Positioning for CantaBio</h2>
            </header>

            <section id="exec-summary" class="scroll-mt-8">
                <div class="bg-white rounded-lg shadow-sm border border-slate-200 p-6 md:p-8">
                    <h3 class="text-lg font-bold text-slate-900 mb-4 uppercase tracking-wider border-b border-slate-100 pb-2">Executive Summary</h3>
                    
                    <p class="text-slate-700 mb-6 leading-relaxed">
                        This section synthesizes the core findings of the 2025–2035 market analysis, providing a high-level overview of the transition dynamics from current amyloid-based standard of care to future tau-targeted therapies. It explicitly outlines the financial scale of the opportunity for CantaBio's CB301 asset.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                        <div class="bg-slate-50 p-5 rounded border border-slate-100 border-l-4 border-l-teal-600">
                            <div class="text-slate-500 text-sm font-medium mb-1">2035 Total Tau Market</div>
                            <div class="text-3xl font-bold text-slate-900">$4.97B</div>
                            <div class="text-xs text-slate-500 mt-2">Emerging primarily post-2030 across all modalities.</div>
                        </div>
                        <div class="bg-slate-50 p-5 rounded border border-slate-100 border-l-4 border-l-sky-600">
                            <div class="text-slate-500 text-sm font-medium mb-1">2035 Aggregation-Modulating Market</div>
                            <div class="text-3xl font-bold text-slate-900">$1.73B</div>
                            <div class="text-xs text-slate-500 mt-2">CantaBio's core addressable segment (unadjusted).</div>
                        </div>
                        <div class="bg-slate-50 p-5 rounded border border-slate-100 border-l-4 border-l-amber-500">
                            <div class="text-slate-500 text-sm font-medium mb-1">Risk-Adjusted Segment Value</div>
                            <div class="text-3xl font-bold text-slate-900">$434M</div>
                            <div class="text-xs text-slate-500 mt-2">Probability-adjusted class market in 2035.</div>
                        </div>
                    </div>

                    <div class="prose max-w-none text-slate-700">
                        <p>Analysis indicates that as of 2026, <strong>there are no approved disease-modifying tau aggregation inhibitor therapies.</strong> The current baseline market is anchored entirely in existing symptomatic therapies and early amyloid biologics. The market opportunity for tau is fundamentally forward-looking and penetration-driven, rather than current revenue-driven.</p>
                        <p class="mt-4">
                            <em>For CantaBio:</em> CB301, functioning as a tau pharmacological chaperone, sits strategically within the aggregation-modulating segment. Value creation relies on navigating clinical evidence hurdles, securing biomarker-gated infrastructure, and competing against parallel mechanisms (amyloid backbones, tau ASOs, and antibodies).
                        </p>
                    </div>
                </div>
            </section>

            <section id="market-transition" class="scroll-mt-8">
                <h3 class="text-2xl font-bold text-slate-900 mb-6 flex items-center">
                    <span class="bg-slate-900 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm mr-3">1</span>
                    Standard of Care to Tau Transition
                </h3>
                
                <p class="text-slate-700 mb-6 leading-relaxed">
                    This section analyzes the chronological shift from the current Standard of Care (SoC)—dominated by symptomatic treatments and amyloid biologics in Alzheimer's Disease (AD)—to the anticipated commercial entry of tau-targeted therapies. It highlights how the future market actually emerges from the existing baseline.
                </p>

                <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200 mb-8">
                    <h4 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4">Evolution of Global Treatment Revenue ($M)</h4>
                    <div class="chart-container">
                        <canvas id="transitionChart"></canvas>
                    </div>
                    <p class="text-sm text-slate-500 italic mt-4 text-center">
                        Analysis indicates tau therapies will primarily act as add-on or replacement therapies in specialized segments post-2030, layering on top of a $19.6B SoC baseline.
                    </p>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full consulting-table bg-white">
                        <thead>
                            <tr>
                                <th>Global Summary by Segment ($M)</th>
                                <th>2025</th>
                                <th>2028</th>
                                <th>2031</th>
                                <th>2035</th>
                                <th>'25–'35 CAGR</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>SoC Market (Pre-Tau Conversion)</td>
                                <td>12,978</td>
                                <td>14,579</td>
                                <td>16,522</td>
                                <td>19,648</td>
                                <td>4.2%</td>
                            </tr>
                            <tr class="bg-teal-50/30">
                                <td>Total Tau-Targeted Market</td>
                                <td>0</td>
                                <td>0</td>
                                <td>125*</td>
                                <td>4,974</td>
                                <td>N/A</td>
                            </tr>
                            <tr class="bg-teal-100/30 font-semibold">
                                <td>Aggregation-Modulating Segment</td>
                                <td>0</td>
                                <td>0</td>
                                <td>43*</td>
                                <td>1,735</td>
                                <td>N/A</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="text-xs text-slate-400 mt-2 text-right">*Initial launch phases commencing 2030-2031 depending on indication (FTD vs AD).</div>
                </div>
            </section>

            <section id="patient-funnel" class="scroll-mt-8">
                <h3 class="text-2xl font-bold text-slate-900 mb-6 flex items-center">
                    <span class="bg-slate-900 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm mr-3">2</span>
                    Patient Funnel & Adoption Constraints
                </h3>
                
                <p class="text-slate-700 mb-6 leading-relaxed">
                    Understanding the total disease burden is insufficient; the commercial opportunity is highly constrained by diagnosis rates, disease stage, and the necessity of biomarker confirmation. This section details the attrition from total prevalence to the net tau-addressable pool.
                </p>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
                        <h4 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-4">Patient Attrition Funnel (Illustrative 2035 Cohort)</h4>
                        <div class="chart-container" style="height: 280px;">
                            <canvas id="funnelChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="flex flex-col justify-center">
                        <div class="space-y-6">
                            <div>
                                <h5 class="font-bold text-slate-900 flex items-center"><span class="text-teal-600 mr-2">&#9654;</span> Diagnosis & Infrastructure</h5>
                                <p class="text-sm text-slate-600 mt-1">U.S. AD diagnosis rate is anchored at 75%, while rare tauopathies like CBD sit at 30%. Infrastructure indices suggest specialized diagnostic pathways (PET/CSF) will severely restrict initial treated pools.</p>
                            </div>
                            <div>
                                <h5 class="font-bold text-slate-900 flex items-center"><span class="text-teal-600 mr-2">&#9654;</span> Biomarker Gating</h5>
                                <p class="text-sm text-slate-600 mt-1"><em>Adoption will not behave like broad primary-care drugs.</em> Therapies require definitive tau confirmation, eliminating large portions of clinically diagnosed but biomarker-negative patients.</p>
                            </div>
                            <div>
                                <h5 class="font-bold text-slate-900 flex items-center"><span class="text-teal-600 mr-2">&#9654;</span> Treatment Role</h5>
                                <p class="text-sm text-slate-600 mt-1">Data suggests tau therapies will switch ~35% of current AD treated patients, while capturing an additional 55% as add-on therapy over existing amyloid or symptomatic backbones.</p>
                            </div>
                        </div>
                    </div>
                </div>

            </section>

            <section id="competitive-dynamics" class="scroll-mt-8">
                <h3 class="text-2xl font-bold text-slate-900 mb-6 flex items-center">
                    <span class="bg-slate-900 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm mr-3">3</span>
                    Competitive Dynamics & Pricing
                </h3>
                
                <p class="text-slate-700 mb-6 leading-relaxed">
                    Tau therapies must compete directly with amyloid-targeting biologics and indirectly with parallel tau mechanisms (ASOs, RNA, Antibodies). This section frameworks the competitive pricing environment and modality distribution required to inform CantaBio's commercial strategy.
                </p>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                    <div class="lg:col-span-2 overflow-x-auto bg-white rounded-lg shadow-sm border border-slate-200 p-1">
                        <table class="w-full consulting-table">
                            <thead>
                                <tr>
                                    <th>Therapy / Modality</th>
                                    <th>Approved Use / Benchmark Type</th>
                                    <th>Value anchor</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Lecanemab (Leqembi)</strong></td>
                                    <td>Early AD; Amyloid confirmed (US Annual WAC)</td>
                                    <td>$26,500</td>
                                </tr>
                                <tr>
                                    <td><strong>Donanemab (Kisunla)</strong></td>
                                    <td>Early AD; Limited-duration course cost</td>
                                    <td>$32,000*</td>
                                </tr>
                                <tr class="bg-slate-50 border-t-2 border-slate-300">
                                    <td><strong>Model: Tau Base Price (AD)</strong></td>
                                    <td>Logical discount applied to amyloid biologics</td>
                                    <td>$22,000</td>
                                </tr>
                                <tr class="bg-slate-50">
                                    <td><strong>Model: Tau Base Price (FTD)</strong></td>
                                    <td>Indication premium (1.15x vs AD)</td>
                                    <td>$25,500</td>
                                </tr>
                                <tr class="bg-slate-50">
                                    <td><strong>Model: Tau Base Price (PSP)</strong></td>
                                    <td>Indication premium (1.2x vs AD)</td>
                                    <td>$26,500</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="text-xs text-slate-400 mt-2 px-2 pb-2">*12-month course example. Pricing implies oral small molecules may trade at a slight discount to biologics but offer higher convenience.</div>
                    </div>

                    <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200 flex flex-col items-center">
                        <h4 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-2 text-center">2035 Total Tau Modality Mix</h4>
                        <div class="text-xs text-slate-500 mb-4 text-center">Total Market: $4.97B</div>
                        <div class="chart-container !h-48 !p-0 !border-0 !shadow-none w-full max-w-[250px]">
                            <canvas id="modalityChart"></canvas>
                        </div>
                        <p class="text-xs text-slate-600 mt-4 text-center">
                            <em>Antibodies and ASOs (e.g., BIIB080) represent the majority share, positioning aggregation-modulators as a differentiated, highly targeted subset.</em>
                        </p>
                    </div>
                </div>
            </section>

            <section id="cantabio-strategy" class="scroll-mt-8">
                <h3 class="text-2xl font-bold text-slate-900 mb-6 flex items-center">
                    <span class="bg-slate-900 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm mr-3">4</span>
                    Strategic Positioning for CantaBio
                </h3>
                
                <p class="text-slate-700 mb-6 leading-relaxed">
                    Where does CantaBio's CB301 fit in this evolving ecosystem? This final section translates the macro landscape into specific strategic imperatives for CB301, leveraging partnering benchmarks and scenario risk-adjustments to recommend a path forward.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                    <div>
                        <div class="bg-teal-900 text-white p-6 rounded-lg shadow-md mb-6">
                            <h4 class="font-bold text-lg mb-3">CB301 Value Proposition</h4>
                            <p class="text-sm text-teal-100 leading-relaxed mb-4">
                                Data suggests CantaBio’s novel small molecules that bind monomeric tau and reduce aggregation place CB301 functionally within the <strong>$1.73B Aggregation-Modulating submarket</strong> (2035 unadjusted).
                            </p>
                            <p class="text-sm text-teal-100 leading-relaxed">
                                <em>Strategic Imperative:</em> Position CB301 as a 'tau-stabilization / anti-aggregation' chaperone, differentiating it from both classic direct inhibitors (which carry historical phase 3 baggage) and invasive ASO/Antibody therapies.
                            </p>
                        </div>

                        <h4 class="text-sm font-bold text-slate-800 uppercase tracking-wider mb-3">Partnering Benchmarks</h4>
                        <div class="bg-white rounded-lg border border-slate-200 overflow-hidden">
                            <table class="w-full text-sm">
                                <tbody>
                                    <tr class="border-b border-slate-100">
                                        <td class="p-3 bg-slate-50 font-medium w-1/3">Deal Proxy</td>
                                        <td class="p-3">ADEL-Y01 / Sanofi (Dec-2025)</td>
                                    </tr>
                                    <tr class="border-b border-slate-100">
                                        <td class="p-3 bg-slate-50 font-medium">Stage / Modality</td>
                                        <td class="p-3">Phase 1 / Tau-targeting antibody</td>
                                    </tr>
                                    <tr>
                                        <td class="p-3 bg-slate-50 font-medium">Economics</td>
                                        <td class="p-3 text-teal-700 font-bold">$80M upfront; up to $1.04B total potential</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
                        <div class="flex justify-between items-center mb-4">
                            <h4 class="text-sm font-bold text-slate-800 uppercase tracking-wider">Aggregation-Modulating Market Scenarios</h4>
                            <div class="text-xs font-semibold px-2 py-1 bg-slate-100 rounded text-slate-600">Risk-Adjusted ($M)</div>
                        </div>
                        <div class="chart-container" style="height: 250px;">
                            <canvas id="scenarioChart"></canvas>
                        </div>
                        <div class="mt-4 text-xs text-slate-600 space-y-2">
                            <p><strong>Base Case (Prob: 1.0x):</strong> Aggregation-modulating class secures $434M risk-adjusted by 2035. Early adoption limited to niche tauopathies and biomarker-enriched AD subsets.</p>
                            <p><strong>Upside Case (Prob: 1.2x):</strong> Accelerated adoption, yielding broader market expansion. Price multipliers (1.1x) combined with success probability multipliers boost trajectory.</p>
                        </div>
                    </div>
                </div>

                <div class="border-t border-slate-200 pt-6">
                    <h4 class="text-lg font-bold text-slate-900 mb-3">Recommendation: Partnering over Solo Commercialization</h4>
                    <p class="text-slate-700 text-sm leading-relaxed mb-4">
                        Analysis indicates that the optimal path for CantaBio is a pre-commercial partnership. The market model demonstrates that the most significant risks lie in infrastructure gating (biomarker rollouts) and commercial competition from deep-pocketed amyloid/ASO players. Securing upfront value via an ADEL-style deal capitalizes on large pharma's sustained strategic appetite for differentiated, oral tau-stabilizing assets before bearing Phase 2/3 capital risk.
                    </p>
                </div>
            </section>
            
            <footer class="pt-12 pb-6 text-center text-xs text-slate-400">
                &copy; 2026 Strategic Advisory. Prepared for CantaBio internal review. Data derived from Market Model and Secondary Research files.
            </footer>

        </div>
    </main>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            
            // --- Navigation Logic ---
            const sections = document.querySelectorAll('section');
            const navLinks = document.querySelectorAll('.nav-link');
            const mobileMenuBtn = document.getElementById('mobile-menu-btn');
            const sidebar = document.getElementById('sidebar');

            // Mobile menu toggle
            mobileMenuBtn.addEventListener('click', () => {
                sidebar.classList.toggle('hidden');
                sidebar.classList.toggle('absolute');
                sidebar.classList.toggle('z-50');
            });

            // Smooth scrolling and active state update
            window.addEventListener('scroll', () => {
                let current = '';
                sections.forEach(section => {
                    const sectionTop = section.offsetTop;
                    const sectionHeight = section.clientHeight;
                    if (scrollY >= (sectionTop - 150)) {
                        current = section.getAttribute('id');
                    }
                });

                navLinks.forEach(link => {
                    link.classList.remove('active-nav', 'bg-slate-800', 'text-white');
                    link.classList.add('text-slate-300');
                    if (link.getAttribute('href').includes(current)) {
                        link.classList.add('active-nav', 'bg-slate-800', 'text-white');
                        link.classList.remove('text-slate-300');
                    }
                });
            });


            // --- Data Definitions (From Source Report) ---
            
            // Chart 1: SoC to Tau Transition
            const transitionData = {
                labels: ['2025', '2028', '2031', '2035'],
                soc: [12978, 14579, 16522, 19648],
                tauTotal: [0, 0, 125, 4974] // Estimating 2031 tau launch start
            };

            // Chart 2: Modality Split (2035)
            // Aggregation Modulators = 1735. Total Tau = 4974. Others = 3239
            const modalityData = {
                labels: ['Aggregation-Modulating (CantaBio Scope)', 'Antibodies, ASOs, & Other Tau'],
                data: [1735, 3239]
            };

            // Chart 3: Patient Funnel Attrition
            const funnelData = {
                labels: ['Prevalent', 'Diagnosed', 'Treated', 'Biomarker Eligible', 'Tau-Treated'],
                data: [100, 75, 40, 15, 5] // Indexed to 100 based on narrative funnel severity
            };

            // Chart 4: Scenarios (Risk Adjusted Aggregation Modulating Market)
            const scenarioData = {
                labels: ['2030', '2031', '2032', '2033', '2034', '2035'],
                base: [0, 4, 25, 110, 240, 434], // Logically interpolated curve up to exact 2035 value
                upside: [0, 6, 35, 145, 320, 572], // Base * 1.1 price * 1.2 prob multiplier approx
                downside: [0, 2, 12, 50, 110, 292] // Base * 0.9 price * 0.75 prob multiplier approx
            };


            // --- Chart Implementations (Chart.js) ---
            
            Chart.defaults.font.family = "'Inter', system-ui, -apple-system, sans-serif";
            Chart.defaults.color = '#64748b'; // slate-500

            // 1. Transition Stacked Bar Chart
            const ctxTransition = document.getElementById('transitionChart').getContext('2d');
            new Chart(ctxTransition, {
                type: 'bar',
                data: {
                    labels: transitionData.labels,
                    datasets: [
                        {
                            label: 'Standard of Care (SoC) Revenue',
                            data: transitionData.soc,
                            backgroundColor: '#334155', // Slate 700
                            borderWidth: 0
                        },
                        {
                            label: 'Total Tau-Targeted Revenue',
                            data: transitionData.tauTotal,
                            backgroundColor: '#0F766E', // Teal 700
                            borderWidth: 0
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { stacked: true, grid: { display: false } },
                        y: { 
                            stacked: true, 
                            grid: { color: '#f1f5f9' },
                            ticks: { callback: function(value) { return '$' + value + 'M'; } }
                        }
                    },
                    plugins: {
                        legend: { position: 'top', labels: { usePointStyle: true, boxWidth: 8 } },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.dataset.label + ': $' + context.parsed.y.toLocaleString() + 'M';
                                }
                            }
                        }
                    }
                }
            });

            // 2. Patient Funnel Chart (Horizontal Bar)
            const ctxFunnel = document.getElementById('funnelChart').getContext('2d');
            new Chart(ctxFunnel, {
                type: 'bar',
                data: {
                    labels: funnelData.labels,
                    datasets: [{
                        label: 'Relative Patient Pool Size (%)',
                        data: funnelData.data,
                        backgroundColor: [
                            '#94A3B8', // Prevalent
                            '#64748B', // Diagnosed
                            '#475569', // Treated
                            '#0F766E', // Biomarker Eligible (Teal)
                            '#042F2E'  // Tau Treated (Dark Teal)
                        ],
                        borderRadius: 4
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { display: false, max: 100 },
                        y: { grid: { display: false }, border: {display: false} }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) { return context.parsed.x + '% of base cohort'; }
                            }
                        }
                    }
                }
            });

            // 3. Modality Split Doughnut Chart
            const ctxModality = document.getElementById('modalityChart').getContext('2d');
            new Chart(ctxModality, {
                type: 'doughnut',
                data: {
                    labels: modalityData.labels,
                    datasets: [{
                        data: modalityData.data,
                        backgroundColor: ['#0EA5E9', '#E2E8F0'], // Sky 500 for CantaBio, Slate 200 for others
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const val = context.parsed;
                                    const total = 4974;
                                    const pct = Math.round((val / total) * 100);
                                    return `$${val}M (${pct}%)`;
                                }
                            }
                        }
                    }
                }
            });

            // 4. Scenario Line Chart
            const ctxScenario = document.getElementById('scenarioChart').getContext('2d');
            new Chart(ctxScenario, {
                type: 'line',
                data: {
                    labels: scenarioData.labels,
                    datasets: [
                        {
                            label: 'Upside Scenario',
                            data: scenarioData.upside,
                            borderColor: '#10B981', // Emerald 500
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                            fill: true,
                            tension: 0.4,
                            borderDash: [5, 5]
                        },
                        {
                            label: 'Base Case',
                            data: scenarioData.base,
                            borderColor: '#0F766E', // Teal 700
                            backgroundColor: 'transparent',
                            borderWidth: 3,
                            tension: 0.4
                        },
                        {
                            label: 'Downside Scenario',
                            data: scenarioData.downside,
                            borderColor: '#EF4444', // Red 500
                            backgroundColor: 'transparent',
                            tension: 0.4,
                            borderDash: [2, 2]
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false } },
                        y: { 
                            grid: { color: '#f1f5f9' },
                            ticks: { callback: function(value) { return '$' + value + 'M'; } }
                        }
                    },
                    plugins: {
                        legend: { position: 'top', labels: { usePointStyle: true, boxWidth: 8 } }
                    }
                }
            });
            
        });
    </script>
</body>
</html>
"""

# Render the HTML using Streamlit Components
# Height is set sufficiently large so the inner scrollbar handles navigation naturally
components.html(HTML_CONTENT, height=1200, scrolling=True)
