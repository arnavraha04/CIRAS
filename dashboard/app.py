import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="CIRAS — Cybercrime Investigation & Record Analysis System",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
.main-header { font-size: 28px; font-weight: bold; color: #FF4B4B; text-align: center; padding: 10px; }
.sub-header { font-size: 14px; color: #888888; text-align: center; margin-bottom: 20px; }
.suspect-box { background-color: #2d0000; border: 2px solid #FF4B4B; border-radius: 8px; padding: 12px 16px; margin: 6px 0; display: flex; align-items: center; justify-content: space-between; }
.suspect-number { font-size: 16px; font-weight: bold; color: #FF4B4B; font-family: monospace; }
.suspect-badge-mastermind { background: #8B0000; color: white; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.suspect-badge-critical { background: #FF0000; color: white; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
.suspect-badge-high { background: #FF8C00; color: white; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">CIRAS — Cybercrime Investigation & Record Analysis System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Telecom Forensics & Network Investigation Platform </div>', unsafe_allow_html=True)

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.mode = None
    for f in ['data/mock_cdr.csv','data/mock_complaints.csv','data/cdr_analysis_result.csv','data/imei_analysis_result.csv','data/suspicious_numbers_imei.csv','data/tower_analysis_result.csv','data/scam_towers.csv','data/graph_analysis_result.csv','data/risk_scores.csv','data/network_graph.html']:
        if os.path.exists(f):
            os.remove(f)

if st.session_state.get('mode') is None:
    st.markdown("---")
    st.markdown("<h2 style='text-align:center;color:white'>Select Investigation Mode</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888'>Choose what type of investigation you want to run</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background:#1a1a2e;border:2px solid #FF4B4B;border-radius:12px;padding:30px;text-align:center;min-height:220px">
            <div style="font-size:50px">🕸️</div>
            <div style="font-size:20px;font-weight:bold;color:#FF4B4B;margin:12px 0">Network Investigation</div>
            <div style="font-size:13px;color:#888;line-height:1.6">
                Analyze large CDR datasets to find scam networks,
                identify masterminds and map criminal operations
            </div>
            <div style="font-size:12px;color:#666;margin-top:12px">
                ✓ Mastermind detection &nbsp; ✓ Network graph<br>
                ✓ Tower hotspot map &nbsp; ✓ Risk scoring
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Network Investigation →", use_container_width=True, key="net_btn"):
            st.session_state.mode = "network"
            st.rerun()
    with col2:
        st.markdown("""
        <div style="background:#1a1a2e;border:2px solid #4B8BFF;border-radius:12px;padding:30px;text-align:center;min-height:220px">
            <div style="font-size:50px">🔎</div>
            <div style="font-size:20px;font-weight:bold;color:#4B8BFF;margin:12px 0">Individual Investigation</div>
            <div style="font-size:13px;color:#888;line-height:1.6">
                Deep dive into one suspect's CDR and IPDR
                to build evidence and prove criminal activity
            </div>
            <div style="font-size:12px;color:#666;margin-top:12px">
                ✓ Call timeline &nbsp; ✓ Movement map<br>
                ✓ IPDR analysis &nbsp; ✓ Evidence profile
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start Individual Investigation →", use_container_width=True, key="ind_btn"):
            st.session_state.mode = "individual"
            st.rerun()
    st.stop()

def data_exists():
    return (
        os.path.exists('data/mock_cdr.csv') and
        os.path.exists('data/risk_scores.csv') and
        os.path.exists('data/tower_analysis_result.csv')
    )

def clear_old_results():
    files_to_clear = [
        'data/mock_cdr.csv','data/mock_complaints.csv',
        'data/cdr_analysis_result.csv','data/imei_analysis_result.csv',
        'data/suspicious_numbers_imei.csv','data/tower_analysis_result.csv',
        'data/scam_towers.csv','data/graph_analysis_result.csv',
        'data/risk_scores.csv','data/network_graph.html',
    ]
    for f in files_to_clear:
        if os.path.exists(f):
            os.remove(f)

def run_analysis(use_complaints=False):
    os.system("python3 analysis/cdr_analysis.py")
    os.system("python3 analysis/imei_analysis.py")
    os.system("python3 analysis/tower_analysis.py")
    os.system("python3 analysis/graph_builder.py")
    if use_complaints:
        os.system("python3 analysis/risk_scorer.py --with-complaints")
    else:
        os.system("python3 analysis/risk_scorer.py")
    os.system("python3 analysis/network_graph.py")

def get_suspected_numbers():
    if not os.path.exists('data/risk_scores.csv'):
        return []
    risk_df = pd.read_csv('data/risk_scores.csv')
    return list(risk_df[risk_df['risk_level'].isin(['MASTERMIND','CRITICAL','HIGH'])]['caller_number'].astype(str))

# Sidebar
st.sidebar.title("Navigation")

if st.session_state.get('mode') == "network":
    st.sidebar.success("🕸️ Network Investigation")
    if st.sidebar.button("← Change Mode"):
        st.session_state.mode = None
        st.rerun()
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Go to", [
        "Upload Data",
        "Overview",
        "Network Graph",
        "CDR Analysis",
        "Risk Scores",
        "Tower Map",
        "IMEI Analysis"
    ])
elif st.session_state.get('mode') == "individual":
    st.sidebar.info("🔎 Individual Investigation")
    if st.sidebar.button("← Change Mode"):
        st.session_state.mode = None
        st.rerun()
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Go to", [
        "Individual - Upload",
        "Individual - Profile",
        "Individual - Timeline",
        "Individual - Movement",
        "Individual - IPDR",
    ])
else:
    page = None

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Status")

if data_exists():
    cdr_count = len(pd.read_csv('data/mock_cdr.csv'))
    st.sidebar.success(f"✓ CDR loaded: {cdr_count:,} records")
    st.sidebar.success("✓ Analysis complete")
    if os.path.exists('data/mock_complaints.csv'):
        st.sidebar.success("✓ Complaints loaded")
    else:
        st.sidebar.warning("○ No complaints file")
    if os.path.exists('data/risk_scores.csv'):
        risk_df = pd.read_csv('data/risk_scores.csv')
        masterminds = risk_df[risk_df['risk_level'] == 'MASTERMIND']
        criticals = risk_df[risk_df['risk_level'] == 'CRITICAL']
        highs = risk_df[risk_df['risk_level'] == 'HIGH']
        if len(masterminds) > 0 or len(criticals) > 0:
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🚨 Suspects")
            for _, row in masterminds.iterrows():
                st.sidebar.error(f"💀 {row['caller_number']}")
            for _, row in criticals.iterrows():
                st.sidebar.error(f"🔴 {row['caller_number']}")
            for _, row in highs.head(3).iterrows():
                st.sidebar.warning(f"🟠 {row['caller_number']}")
else:
    st.sidebar.error("✗ No data loaded")
    st.sidebar.info("Go to Upload Data to begin")

if page == "Upload Data":
    st.subheader("Upload Investigation Data")

    st.markdown("### CDR File (Required)")
    st.markdown("Your CDR CSV must have these columns:")
    st.code("caller_number, receiver_number, call_duration_secs, timestamp, tower_id, imei")
    cdr_file = st.file_uploader("Upload CDR CSV", type=['csv'], key='cdr')

    st.markdown("---")
    st.markdown("### Complaints File (Optional)")
    st.info("Adding complaints increases risk scoring accuracy from 100 to 130 points maximum.")
    complaints_file = st.file_uploader("Upload Complaints CSV (optional)", type=['csv'], key='complaints')

    st.markdown("---")
    st.markdown("### Run Analysis")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Use Mock Data (Demo Mode)", use_container_width=True):
            with st.spinner("Clearing old data..."):
                clear_old_results()
            with st.spinner("Generating fresh mock data..."):
                os.system("python3 data/mock_data_generator.py")
            progress = st.progress(0, text="Starting demo analysis...")
            progress.progress(10, text="Generating mock data...")
            os.system("python3 data/mock_data_generator.py")
            progress.progress(25, text="Running CDR analysis...")
            os.system("python3 analysis/cdr_analysis.py")
            progress.progress(40, text="Running IMEI analysis...")
            os.system("python3 analysis/imei_analysis.py")
            progress.progress(55, text="Running tower analysis...")
            os.system("python3 analysis/tower_analysis.py")
            progress.progress(70, text="Building call graph...")
            os.system("python3 analysis/graph_builder.py")
            progress.progress(82, text="Calculating risk scores...")
            os.system("python3 analysis/risk_scorer.py --with-complaints")
            progress.progress(92, text="Building network graph...")
            os.system("python3 analysis/network_graph.py")
            progress.progress(100, text="Done!")
            st.success("Demo analysis complete. Go to Overview.")
            st.rerun()

    with col2:
        if st.button("Run Analysis", use_container_width=True):
            if cdr_file is None:
                st.error("Please upload a CDR file to continue.")
            else:
                required_cdr_cols = ['caller_number','receiver_number','call_duration_secs','timestamp','tower_id','imei']
                cdr_df = pd.read_csv(cdr_file)
                missing = [c for c in required_cdr_cols if c not in cdr_df.columns]
                if missing:
                    st.error(f"CDR file missing columns: {missing}")
                else:
                    with st.spinner("Clearing old results..."):
                        clear_old_results()
                    with st.spinner("Saving uploaded CDR..."):
                        cdr_df.to_csv('data/mock_cdr.csv', index=False)
                        st.success(f"CDR uploaded: {len(cdr_df):,} records")
                    use_complaints = False
                    if complaints_file is not None:
                        complaints_df = pd.read_csv(complaints_file)
                        complaints_df.to_csv('data/mock_complaints.csv', index=False)
                        st.success(f"Complaints uploaded: {len(complaints_df):,} records")
                        use_complaints = True
                    else:
                        st.info("CDR-only mode — max score: 100")
                    progress = st.progress(0, text="Starting analysis...")
                    progress.progress(10, text="Running CDR analysis...")
                    os.system("python3 analysis/cdr_analysis.py")
                    progress.progress(30, text="Running IMEI analysis...")
                    os.system("python3 analysis/imei_analysis.py")
                    progress.progress(50, text="Running tower analysis...")
                    os.system("python3 analysis/tower_analysis.py")
                    progress.progress(65, text="Building call graph...")
                    os.system("python3 analysis/graph_builder.py")
                    progress.progress(80, text="Calculating risk scores...")
                    if use_complaints:
                        os.system("python3 analysis/risk_scorer.py --with-complaints")
                    else:
                        os.system("python3 analysis/risk_scorer.py")
                    progress.progress(90, text="Building network graph...")
                    os.system("python3 analysis/network_graph.py")
                    progress.progress(100, text="Done!")
                    st.success("Analysis complete. Go to Overview.")
                    st.balloons()
                    st.rerun()

    st.markdown("---")
    if data_exists():
        st.warning("Current data is loaded. Uploading new data will replace it completely.")
    else:
        st.info("No data loaded. Upload a CDR file or click Demo Mode to begin.")

elif page == "Overview":
    if not data_exists():
        st.markdown("## Welcome")
        st.markdown("No investigation data loaded yet.")
        st.markdown("Go to **Upload Data** in the sidebar to get started.")
        st.stop()

    cdr_df = pd.read_csv('data/mock_cdr.csv')
    risk_df = pd.read_csv('data/risk_scores.csv')
    tower_df = pd.read_csv('data/tower_analysis_result.csv')
    has_complaints = os.path.exists('data/mock_complaints.csv')
    suspected = get_suspected_numbers()

    st.subheader("Investigation Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total CDR Records", f"{len(cdr_df):,}")
    with col2:
        if has_complaints:
            complaints_df = pd.read_csv('data/mock_complaints.csv')
            st.metric("Total Complaints", f"{len(complaints_df):,}")
        else:
            st.metric("Total Complaints", "N/A")
    with col3:
        critical = len(risk_df[risk_df['risk_level'].isin(['MASTERMIND','CRITICAL'])])
        st.metric("CRITICAL Numbers", critical, delta="Immediate Action")
    with col4:
        st.metric("Towers Analyzed", len(tower_df))

    st.markdown("---")
    if suspected:
        st.subheader("🚨 Suspected Numbers — Immediate Attention Required")
        for num in suspected:
            rows = risk_df[risk_df['caller_number'].astype(str) == str(num)]
            if len(rows) == 0:
                continue
            row = rows.iloc[0]
            level = row['risk_level']
            badge_class = f"suspect-badge-{level.lower()}"
            st.markdown(f"""
            <div class="suspect-box">
                <span class="suspect-number">📵 {num}</span>
                <span style="color:#aaaaaa;font-size:13px">Score: {int(row['total_risk_score'])}/{int(row['max_possible_score'])} | Victims: {int(row['unique_victims_called'])} | Calls: {int(row['total_outgoing_calls'])}</span>
                <span class="{badge_class}">{level}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

    st.subheader("Suspected Mastermind")
    mastermind = risk_df.iloc[0]
    max_score = int(mastermind['max_possible_score'])
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.error(f"Phone: {mastermind['caller_number']}")
    with col2:
        st.error(f"Risk Score: {mastermind['total_risk_score']}/{max_score}")
    with col3:
        st.error(f"Risk Level: {mastermind['risk_level']}")
    with col4:
        st.error(f"Victims Called: {int(mastermind['unique_victims_called'])}")

    st.markdown("---")
    if has_complaints:
        complaints_df = pd.read_csv('data/mock_complaints.csv')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Agency Impersonation")
            agency_counts = complaints_df['agency_impersonated'].value_counts().reset_index()
            agency_counts.columns = ['Agency', 'Count']
            fig = px.pie(agency_counts, values='Count', names='Agency',
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.subheader("Amount Lost by Agency (INR)")
            amount_by_agency = complaints_df.groupby('agency_impersonated')['amount_lost_inr'].sum().reset_index()
            amount_by_agency.columns = ['Agency', 'Total Amount Lost']
            fig2 = px.bar(amount_by_agency, x='Agency', y='Total Amount Lost',
                          color='Total Amount Lost', color_continuous_scale='Reds')
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.subheader("Call Volume by Hour")
        cdr_df['hour'] = pd.to_datetime(cdr_df['timestamp']).dt.hour
        hourly = cdr_df.groupby('hour').size().reset_index()
        hourly.columns = ['Hour', 'Call Count']
        fig = px.bar(hourly, x='Hour', y='Call Count',
                     color='Call Count', color_continuous_scale='Reds',
                     title='Call volume by hour of day')
        st.plotly_chart(fig, use_container_width=True)

elif page == "Suspect Watch List":
    if not data_exists():
        st.warning("No data loaded. Go to Upload Data first.")
        st.stop()

    risk_df = pd.read_csv('data/risk_scores.csv')
    cdr_df = pd.read_csv('data/mock_cdr.csv')
    suspected = get_suspected_numbers()

    st.subheader("🚨 Suspect Watch List")
    if not suspected:
        st.info("No suspected numbers found.")
        st.stop()

    mastermind_df = risk_df[risk_df['risk_level'] == 'MASTERMIND']
    critical_df = risk_df[risk_df['risk_level'] == 'CRITICAL']
    high_df = risk_df[risk_df['risk_level'] == 'HIGH']

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("MASTERMIND", len(mastermind_df))
    with col2:
        st.metric("CRITICAL", len(critical_df))
    with col3:
        st.metric("HIGH", len(high_df))
    with col4:
        total_victims = risk_df[risk_df['caller_number'].astype(str).isin(suspected)]['unique_victims_called'].sum()
        st.metric("Total Victims", int(total_victims))

    st.markdown("---")
    for num in suspected:
        rows = risk_df[risk_df['caller_number'].astype(str) == str(num)]
        if len(rows) == 0:
            continue
        row = rows.iloc[0]
        level = row['risk_level']
        icon = '💀' if level == 'MASTERMIND' else '🔴' if level == 'CRITICAL' else '🟠'
        calls_made = cdr_df[cdr_df['caller_number'].astype(str) == str(num)]

        with st.expander(f"{icon} {num} — {level} | Score: {int(row['total_risk_score'])}/{int(row['max_possible_score'])}"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Outgoing Calls", int(row['total_outgoing_calls']))
            with col2:
                st.metric("Unique Victims", int(row['unique_victims_called']))
            with col3:
                avg = calls_made['call_duration_secs'].mean() if len(calls_made) > 0 else 0
                st.metric("Avg Duration", f"{avg:.0f}s")
            with col4:
                st.metric("Risk Score", f"{int(row['total_risk_score'])}/{int(row['max_possible_score'])}")
            if len(calls_made) > 0:
                st.markdown("**Towers used:**")
                towers_used = calls_made['tower_id'].value_counts().reset_index()
                towers_used.columns = ['Tower', 'Calls']
                st.dataframe(towers_used, use_container_width=True)
                st.markdown("**Recent calls:**")
                st.dataframe(calls_made[['receiver_number','call_duration_secs','timestamp','tower_id']].head(10), use_container_width=True)

elif page == "Network Graph":
    if not data_exists():
        st.warning("No data loaded. Go to Upload Data first.")
        st.stop()

    st.subheader("Call Network Graph")
    st.markdown("💀 Dark red = Mastermind | 🔴 Red = CRITICAL | 🟠 Orange = HIGH | Grey = Victims")

    if os.path.exists('data/risk_scores.csv'):
        risk_df = pd.read_csv('data/risk_scores.csv')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("MASTERMIND", len(risk_df[risk_df['risk_level'] == 'MASTERMIND']))
        with col2:
            st.metric("CRITICAL", len(risk_df[risk_df['risk_level'] == 'CRITICAL']))
        with col3:
            st.metric("HIGH", len(risk_df[risk_df['risk_level'] == 'HIGH']))

    if st.button("Regenerate Graph"):
        with st.spinner("Rebuilding..."):
            os.system("python3 analysis/network_graph.py")
        st.rerun()

    st.markdown("---")
    if not os.path.exists('data/network_graph.html'):
        with st.spinner("Building network graph..."):
            os.system("python3 analysis/network_graph.py")
        st.rerun()

    with open('data/network_graph.html', 'r') as f:
        graph_html = f.read()
    components.html(graph_html, height=650, scrolling=True)

elif page == "CDR Analysis":
    if not data_exists():
        st.warning("No data loaded. Go to Upload Data first.")
        st.stop()

    cdr_df = pd.read_csv('data/mock_cdr.csv')
    suspected = get_suspected_numbers()

    st.subheader("Call Detail Records Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Calls", f"{len(cdr_df):,}")
    with col2:
        st.metric("Unique Numbers", cdr_df['caller_number'].nunique())
    with col3:
        st.metric("Avg Duration", f"{cdr_df['call_duration_secs'].mean():.0f}s")

    st.markdown("---")
    cdr_df['hour'] = pd.to_datetime(cdr_df['timestamp']).dt.hour
    hourly = cdr_df.groupby('hour').size().reset_index()
    hourly.columns = ['Hour', 'Call Count']
    fig = px.bar(hourly, x='Hour', y='Call Count',
                 title='Call volume by hour of day',
                 color='Call Count', color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 20 Most Active Callers")
    top_callers = cdr_df['caller_number'].value_counts().head(20).reset_index()
    top_callers.columns = ['Phone Number', 'Call Count']
    fig2 = px.bar(top_callers, x='Phone Number', y='Call Count',
                  color=top_callers['Phone Number'].astype(str).isin(suspected).map({True:'Suspected',False:'Normal'}),
                  color_discrete_map={'Suspected':'#FF0000','Normal':'#4B8BFF'},
                  title='Top 20 callers — red = suspected scammer')
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Raw CDR Data (suspected numbers highlighted)")
    display_df = cdr_df.head(200).copy()
    display_df['caller_number'] = display_df['caller_number'].astype(str)
    styled = display_df.style.apply(
        lambda row: ['background-color: #3d0000; color: #FF6B6B; font-weight: bold'
                     if str(row['caller_number']) in suspected else '' for _ in row], axis=1)
    st.dataframe(styled, use_container_width=True)

elif page == "Risk Scores":
    if not data_exists():
        st.warning("No data loaded. Go to Upload Data first.")
        st.stop()

    risk_df = pd.read_csv('data/risk_scores.csv')
    max_score = int(risk_df['max_possible_score'].iloc[0])

    st.subheader(f"Suspect Risk Scoring (Max: {max_score} points)")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("MASTERMIND", len(risk_df[risk_df['risk_level'] == 'MASTERMIND']))
    with col2:
        st.metric("CRITICAL", len(risk_df[risk_df['risk_level'] == 'CRITICAL']))
    with col3:
        st.metric("HIGH", len(risk_df[risk_df['risk_level'] == 'HIGH']))
    with col4:
        st.metric("MEDIUM", len(risk_df[risk_df['risk_level'] == 'MEDIUM']))
    with col5:
        st.metric("LOW", len(risk_df[risk_df['risk_level'] == 'LOW']))

    st.markdown("---")
    top_suspects = risk_df.head(20)
    fig = px.bar(top_suspects, x='caller_number', y='total_risk_score',
                 color='risk_level',
                 color_discrete_map={'MASTERMIND':'#8B0000','CRITICAL':'#FF0000','HIGH':'#FF8C00','MEDIUM':'#FFD700','LOW':'#00CC44'},
                 title='Top 20 suspects by risk score')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Full Suspect List")
    def highlight_risk(row):
        if row['risk_level'] == 'MASTERMIND':
            return ['background-color: #4d0000; color: #FF0000; font-weight: bold'] * len(row)
        elif row['risk_level'] == 'CRITICAL':
            return ['background-color: #3d0000; color: #FF6B6B; font-weight: bold'] * len(row)
        elif row['risk_level'] == 'HIGH':
            return ['background-color: #3d1a00; color: #FFB347; font-weight: bold'] * len(row)
        elif row['risk_level'] == 'MEDIUM':
            return ['background-color: #2d2d00; color: #FFD700'] * len(row)
        return [''] * len(row)

    display_cols = ['caller_number','total_risk_score','risk_level','total_outgoing_calls','unique_victims_called']
    styled_df = risk_df[display_cols].head(50).style.apply(highlight_risk, axis=1)
    st.dataframe(styled_df, use_container_width=True)

elif page == "Tower Map":
    if not data_exists():
        st.warning("No data loaded. Go to Upload Data first.")
        st.stop()

    tower_df = pd.read_csv('data/tower_analysis_result.csv')
    scam_towers_df = pd.read_csv('data/scam_towers.csv')
    tower_df['is_scam_tower'] = tower_df['tower_id'].isin(scam_towers_df['tower_id'])

    st.subheader("Cell Tower Movement Map")
    st.markdown("🔴 Red = Scam hotspot | 🔵 Blue = Normal tower | Click markers for details")

    m = folium.Map(location=[28.6139, 77.2090], zoom_start=8)
    for _, row in tower_df.iterrows():
        color = 'red' if row['is_scam_tower'] else 'blue'
        radius = 25 if row['is_scam_tower'] else 15
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            color=color, fill=True, fill_color=color, fill_opacity=0.8, weight=3,
            popup=folium.Popup(
                f"<b>Tower:</b> {row['tower_id']}<br>"
                f"<b>Total Calls:</b> {row['total_calls']}<br>"
                f"<b>Unique Callers:</b> {row['unique_callers']}<br>"
                f"<b>Scam Tower:</b> {'YES' if row['is_scam_tower'] else 'NO'}",
                max_width=200)
        ).add_to(m)
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['tower_id'],
            icon=folium.DivIcon(
                html=f'<div style="font-size:10px;color:white;background:{"red" if row["is_scam_tower"] else "#1a5276"};padding:2px 6px;border-radius:3px;white-space:nowrap;margin-top:-10px">{row["tower_id"]}</div>'
            )
        ).add_to(m)
    st_folium(m, width=750, height=550)

    st.markdown("---")
    st.subheader("Tower Activity Table")
    st.dataframe(tower_df, use_container_width=True)

elif page == "IMEI Analysis":
    if not data_exists():
        st.warning("No data loaded. Go to Upload Data first.")
        st.stop()

    imei_df = pd.read_csv('data/imei_analysis_result.csv')
    st.subheader("IMEI Device Correlation")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Unique IMEIs", len(imei_df))
    with col2:
        st.metric("Multi-SIM Devices", len(imei_df[imei_df['multi_sim_flag'] == True]))

    st.markdown("---")
    top_imei = imei_df.sort_values('unique_sims', ascending=False).head(10)
    fig = px.bar(top_imei, x='imei', y='unique_sims',
                 color='unique_sims', color_continuous_scale='Reds',
                 title='Top 10 devices with most SIM cards')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Full IMEI Table")
    st.dataframe(imei_df.sort_values('unique_sims', ascending=False), use_container_width=True)


if st.session_state.get('mode') == "individual":

    if page == "Individual - Upload":
        st.subheader("Individual Investigation")
        st.markdown("### Suspect Phone Number")
        suspect_number = st.text_input("Enter suspect phone number", placeholder="e.g. 9876543210")
        st.session_state.suspect_number = suspect_number

        st.markdown("### CDR File")
        st.code("caller_number, receiver_number, call_duration_secs, timestamp, tower_id, imei")
        cdr_file = st.file_uploader("Upload CDR CSV", type=['csv'], key='ind_cdr')

        st.markdown("### IPDR File (Optional)")
        st.code("phone_number, timestamp, site_visited, app_used, data_used_mb, session_duration, vpn_detected, ip_address")
        ipdr_file = st.file_uploader("Upload IPDR CSV (optional)", type=['csv'], key='ind_ipdr')

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Use Mock Data", use_container_width=True):
                with st.spinner("Generating mock data..."):
                    os.system("python3 data/mock_data_generator.py")
                    os.system("python3 data/generate_ipdr.py")
                with st.spinner("Running investigation..."):
                    os.system("python3 analysis/individual_investigation.py")
                st.session_state.suspect_number = '9876543210'
                st.success("Done. Go to Individual - Profile.")
                st.rerun()

        with col2:
            if st.button("Run Investigation", use_container_width=True):
                if not suspect_number:
                    st.error("Please enter a suspect phone number.")
                elif cdr_file is None:
                    st.error("Please upload a CDR file.")
                else:
                    cdr_df = pd.read_csv(cdr_file)
                    cdr_df.to_csv('data/mock_cdr.csv', index=False)
                    if ipdr_file is not None:
                        ipdr_df = pd.read_csv(ipdr_file)
                        ipdr_df.to_csv('data/mock_ipdr.csv', index=False)
                    with st.spinner("Running investigation..."):
                        import sys
                        sys.path.append('analysis')
                        from individual_investigation import run_individual_investigation
                        run_individual_investigation(
                            cdr_path='data/mock_cdr.csv',
                            suspect_number=suspect_number,
                            ipdr_path='data/mock_ipdr.csv' if ipdr_file else None
                        )
                    st.success("Done. Go to Individual - Profile.")
                    st.rerun()

    elif page == "Individual - Profile":
        suspect = st.session_state.get('suspect_number', '9876543210')
        st.subheader(f"Suspect Profile — {suspect}")

        if not os.path.exists('data/individual_contacts.csv'):
            st.warning("No investigation data. Go to Individual - Upload first.")
            st.stop()

        contacts = pd.read_csv('data/individual_contacts.csv')
        timeline = pd.read_csv('data/individual_timeline.csv')
        hourly = pd.read_csv('data/individual_hourly.csv')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Calls", len(timeline))
        with col2:
            outgoing = timeline[timeline['direction'] == 'OUTGOING']
            st.metric("Outgoing", len(outgoing))
        with col3:
            incoming = timeline[timeline['direction'] == 'INCOMING']
            st.metric("Incoming", len(incoming))
        with col4:
            st.metric("Unique Contacts", len(contacts))

        st.markdown("---")
        st.subheader("Top 10 Contacts")
        fig = px.bar(contacts.head(10), x='contact_number', y='total_calls',
                     color='total_calls', color_continuous_scale='Reds',
                     title='Most frequently contacted numbers')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Call Activity by Hour")
        fig2 = px.bar(hourly, x='hour', y='call_count',
                      color='call_count', color_continuous_scale='Reds',
                      title='When was suspect most active')
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("All Contacts")
        st.dataframe(contacts, use_container_width=True)

    elif page == "Individual - Timeline":
        suspect = st.session_state.get('suspect_number', '9876543210')
        st.subheader(f"Call Timeline — {suspect}")

        if not os.path.exists('data/individual_timeline.csv'):
            st.warning("No investigation data. Go to Individual - Upload first.")
            st.stop()

        timeline = pd.read_csv('data/individual_timeline.csv')
        timeline['timestamp'] = pd.to_datetime(timeline['timestamp'])

        st.metric("Total Events", len(timeline))
        st.markdown("---")

        st.subheader("Call Timeline")
        fig = px.scatter(timeline, x='timestamp', y='call_duration_secs',
                         color='direction',
                         color_discrete_map={'OUTGOING':'#FF4444','INCOMING':'#4444FF'},
                         hover_data=['other_number','tower_id'],
                         title='Every call plotted on timeline')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Raw Timeline")
        st.dataframe(timeline, use_container_width=True)

    elif page == "Individual - Movement":
        suspect = st.session_state.get('suspect_number', '9876543210')
        st.subheader(f"Movement Map — {suspect}")

        if not os.path.exists('data/individual_movement.csv'):
            st.warning("No investigation data. Go to Individual - Upload first.")
            st.stop()

        movement = pd.read_csv('data/individual_movement.csv')

        tower_coordinates = {
            'TWR_DEL_ROHINI_01':  (28.7041, 77.1025),
            'TWR_DEL_ROHINI_02':  (28.7080, 77.1100),
            'TWR_DEL_DWARKA_01':  (28.5921, 77.0460),
            'TWR_DEL_CP_01':      (28.6315, 77.2167),
            'TWR_NOI_SEC15_01':   (28.5700, 77.3200),
            'TWR_NOI_SEC62_01':   (28.6270, 77.3650),
            'TWR_MUM_ANDHERI_01': (19.1136, 72.8697),
            'TWR_MUM_THANE_01':   (19.2183, 72.9781),
            'TWR_DEL_001':        (28.6139, 77.2090),
            'TWR_DEL_002':        (28.6200, 77.2150),
            'TWR_MUM_001':        (19.0760, 72.8777),
            'TWR_MUM_002':        (19.0800, 72.8800),
        }

        movement['latitude'] = movement['tower_id'].map(
            lambda x: tower_coordinates.get(x, (28.6139, 77.2090))[0])
        movement['longitude'] = movement['tower_id'].map(
            lambda x: tower_coordinates.get(x, (28.6139, 77.2090))[1])

        st.metric("Towers Visited", len(movement))
        st.markdown("🔴 Bigger = more calls from that tower")
        st.markdown("---")

        m = folium.Map(location=[25.0, 77.0], zoom_start=5)
        max_calls = movement['total_calls'].max()

        for _, row in movement.iterrows():
            radius = int(10 + (row['total_calls'] / max_calls) * 30)
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=radius,
                color='red', fill=True, fill_color='red', fill_opacity=0.7,
                popup=folium.Popup(
                    f"<b>Tower:</b> {row['tower_id']}<br>"
                    f"<b>Calls:</b> {row['total_calls']}<br>"
                    f"<b>First seen:</b> {row['first_seen']}<br>"
                    f"<b>Last seen:</b> {row['last_seen']}",
                    max_width=200)
            ).add_to(m)
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                icon=folium.DivIcon(
                    html=f'<div style="font-size:10px;color:white;background:red;padding:2px 5px;border-radius:3px">{row["tower_id"]}</div>'
                )
            ).add_to(m)

        st_folium(m, width=750, height=500)

        st.markdown("---")
        st.subheader("Movement Table")
        st.dataframe(movement[['tower_id','total_calls','first_seen','last_seen']], use_container_width=True)

    elif page == "Individual - IPDR":
        suspect = st.session_state.get('suspect_number', '9876543210')
        st.subheader(f"IPDR Analysis — {suspect}")

        if not os.path.exists('data/individual_sites.csv'):
            st.warning("No IPDR data found. Upload an IPDR file or use mock data.")
            st.stop()

        sites = pd.read_csv('data/individual_sites.csv')
        apps = pd.read_csv('data/individual_apps.csv')

        suspicious_sites = sites[sites['suspicious'] == True]
        suspicious_apps = apps[apps['suspicious'] == True]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sites Visited", len(sites))
        with col2:
            st.metric("Suspicious Sites", len(suspicious_sites))
        with col3:
            st.metric("Suspicious Apps", len(suspicious_apps))

        st.markdown("---")

        if len(suspicious_sites) > 0:
            st.error("⚠️ Suspicious websites detected")
            st.dataframe(suspicious_sites[['site_visited','visits','total_data_mb']], use_container_width=True)

        if len(suspicious_apps) > 0:
            st.error("⚠️ Suspicious apps detected")
            st.dataframe(suspicious_apps[['app_used','sessions','total_data_mb']], use_container_width=True)

        st.markdown("---")
        st.subheader("Top Sites Visited")
        fig = px.bar(sites.head(15), x='site_visited', y='visits',
                     color='suspicious',
                     color_discrete_map={True:'#FF0000', False:'#4444FF'},
                     title='Red = suspicious sites')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("App Usage")
        fig2 = px.bar(apps.head(15), x='app_used', y='sessions',
                      color='suspicious',
                      color_discrete_map={True:'#FF0000', False:'#4444FF'},
                      title='Red = suspicious apps')
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)

