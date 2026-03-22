import os
import streamlit as st

from services.jira_client import fetch_issues
from utils.data_processing import issues_to_dataframe
from domain.safe_metrics import *
from ui.team_view import render_teams

st.set_page_config(
    page_title="ART Progress Dashboard",
    page_icon="📊", 
    layout="wide"
)

st.title("🚀 Afya - Quarter Tracking")

label = st.text_input(
    "Label do Épico",
    value="EpicoPI1Legado"
)

if not label:
    st.warning("Informe uma label para buscar os épicos.")
    st.stop()

jql = f"""
labels = {label} AND issuetype = Epic
"""

with st.spinner("Carregando dados do Jira..."):
    issues, epic_map = fetch_issues(jql)

df = issues_to_dataframe(issues)

epic_progress = calculate_epic_progress(df)
team_progress = calculate_team_progress(epic_progress)

teams = sorted(team_progress["team"].unique())

selected_teams = st.sidebar.multiselect(
    "Filtrar Squads",
    teams,
    default=teams
)

filtered_epic_progress = epic_progress[
    epic_progress["team"].isin(selected_teams)
]

filtered_team_progress = team_progress[
    team_progress["team"].isin(selected_teams)
]

cluster_progress = calculate_cluster_progress(filtered_team_progress)

quarter_time_progress = calculate_quarter_time_progress()

squads_at_risk, epics_at_risk, total_epics = calculate_risk_metrics(
    filtered_epic_progress,
    filtered_team_progress,
    quarter_time_progress
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Progresso de Épicos", f"{cluster_progress:.1f}%")
col2.metric("% Tempo decorrido (quarter)", f"{quarter_time_progress:.1f}%")
col3.metric("Potenciais squads em risco", squads_at_risk)
col4.metric("Potenciais épicos em risco", f"{epics_at_risk} / {total_epics}")

render_teams(
    filtered_team_progress,
    filtered_epic_progress,
    epic_map,
    df
)