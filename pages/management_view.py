import streamlit as st
import pandas as pd
from utils.period_utils import get_default_cycle, get_quarter_dates
from ui.roadmap_view import render_roadmap
from services.jira_client import fetch_issues
from utils.data_processing import issues_to_dataframe
from domain.safe_metrics import *
from utils.label_options import *
from utils.sprint_config import get_sprints
from utils.roadmap_processing import build_roadmap_dataframe
from ui.team_view import render_teams
from utils.dashboard_filters import get_available_teams, filter_by_teams

st.set_page_config(page_title="Quarter Roadmap", layout="wide")

st.title("🚀 Afya - Quarter Roadmap")

label_options = get_label_options()

selected_product = st.selectbox(
    "Produto",
    get_products(label_options)
)

available_cycles = get_cycles(label_options, selected_product)
default_cycle = get_default_cycle(available_cycles)

selected_cycle = st.selectbox(
    "Quarter / PI",
    available_cycles,
    index=available_cycles.index(default_cycle)
)

selection = get_selection(label_options, selected_product, selected_cycle)

labels = selection["labels"]

quarter = selection["quarter"]
year = selection["year"]

sprints = get_sprints(quarter, year)

start_date, end_date = get_quarter_dates(year, quarter)
quarter_time_progress = calculate_quarter_time_progress(start_date, end_date)
selected_period_label = f"{quarter}/{year}"

st.caption(f"Filtro aplicado: {selected_product} | {selected_cycle}")

if st.button("🔄 Atualizar dados"):
    st.cache_data.clear()
    st.rerun()

labels_jql = ", ".join(labels)

jql = f"""
labels in ({labels_jql}) AND issuetype in (Epic,"Enabler Epic")
"""

with st.spinner("Carregando dados do Jira..."):
    issues, epic_map, epic_df = fetch_issues(jql)

df = issues_to_dataframe(issues)

epic_progress = calculate_epic_progress(df)

epic_progress = epic_df.merge(
    epic_progress,
    on="epic",
    how="left"
)

epics_with_children = set(epic_progress["epic"].unique())
empty_epics = epic_df[~epic_df["epic"].isin(epics_with_children)].copy()

if not empty_epics.empty:
    empty_epics["epic_owner_team"] = empty_epics["team"]
    empty_epics["completed_items"] = 0
    empty_epics["total_items"] = 0
    empty_epics["progress"] = 0.0

    epic_progress = pd.concat(
        [epic_progress, empty_epics],
        ignore_index=True,
        sort=False
    )

epic_progress["completed_items"] = epic_progress["completed_items"].fillna(0).astype(int)
epic_progress["total_items"] = epic_progress["total_items"].fillna(0).astype(int)
epic_progress["progress"] = epic_progress["progress"].fillna(0.0)
team_progress = calculate_team_progress(epic_progress)

roadmap_df = build_roadmap_dataframe(epic_progress, epic_df, epic_map)

#roadmap_df = roadmap_df.dropna(subset=["start_date", "end_date"])

teams = get_available_teams(team_progress)

selected_teams = st.sidebar.multiselect(
    "Filtrar Squads",
    teams,
    default=teams
)

only_with_dates = st.sidebar.toggle(
    "Exibir somente épicos com datas",
    value=False
)

filtered_epic_progress, filtered_team_progress = filter_by_teams(
    epic_progress,
    team_progress,
    selected_teams
)

roadmap_df = roadmap_df[
    roadmap_df["team"].isin(selected_teams)
]

if only_with_dates:
    roadmap_df = roadmap_df.dropna(subset=["start_date", "end_date"])

summary_df = roadmap_df.drop_duplicates(subset=["epic"]).copy()

total_epics = summary_df["epic"].nunique()

completed_count = summary_df[
    summary_df["progress"] >= 100
]["epic"].nunique()

delayed_count = summary_df[
    summary_df["roadmap_status"] == "Atrasado"
]["epic"].nunique()

in_progress_count = summary_df[
    (summary_df["progress"] < 100) &
    (summary_df["roadmap_status"] != "Atrasado")
]["epic"].nunique()

completion_rate = 0

if total_epics > 0:
    completion_rate = (completed_count / total_epics) * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("% Épicos concluídos", f"{completion_rate:.1f}%")
col2.metric("⏰ Épicos atrasados", delayed_count)
col3.metric("✅ Concluídos", completed_count)
col4.metric("🔵 Em andamento", in_progress_count)
col5.metric("📦 Total de épicos", total_epics)

st.caption("⏱️ Dados atualizados a cada 5 minutos")

render_roadmap(
    roadmap_df,
    start_date=start_date,
    end_date=end_date,
    quarter_time_progress=quarter_time_progress,
    sprints=sprints
)

st.divider()

st.subheader(f"📋 Visão operacional ({total_epics} épicos)")

with st.container():
    render_teams(
        filtered_team_progress,
        filtered_epic_progress,
        epic_map,
        df
    )