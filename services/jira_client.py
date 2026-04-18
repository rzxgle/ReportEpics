import streamlit as st
from jira import JIRA
import pandas as pd
from config import *


def get_jira_client():

    return JIRA(
        server=JIRA_URL,
        basic_auth=(JIRA_EMAIL, JIRA_TOKEN)
    )

@st.cache_data(ttl=300, show_spinner=False)
def fetch_issues(jql):

    jira = get_jira_client()

    epics = jira.search_issues(
        jql,
        maxResults=False,
        fields=[
            "summary", 
            "labels", 
            TEAM_FIELD, # campo team
            "customfield_11806", # Épico em risco
            "customfield_11839", # Motivo do risco
            "customfield_10505", # data inicio do épico
            "duedate" # data fim do épico
            ] 
    )

    epic_map = {epic.key: epic.fields.summary for epic in epics}

    epic_data = []

    for epic in epics:
        team_obj = getattr(epic.fields, TEAM_FIELD, None)
        team = team_obj.name if team_obj else "Team Desconhecido"
        risk_obj = getattr(epic.fields, "customfield_11806", None)
        risk_value = getattr(risk_obj, "value", None) if risk_obj else None
        risk_reason = getattr(epic.fields, "customfield_11839", None)
        epic_labels = getattr(epic.fields, "labels", []) or []
        is_transbordo = "LegadoTransbordoP126" in epic_labels
        start_date = getattr(epic.fields, "customfield_10505", None)
        end_date = getattr(epic.fields, "duedate", None)

        epic_data.append({
            "epic": epic.key,
            "team": team,
            "epic_risk": risk_value == "Sim",
            "epic_risk_reason": risk_reason if risk_reason else "",
            "is_transbordo": is_transbordo,
            "start_date": start_date,
            "end_date": end_date
        })

    epic_df = pd.DataFrame(epic_data)

    epic_keys = list(epic_map.keys())

    if not epic_keys:
        return [], {}, epic_df

    epic_string = ",".join(epic_keys)

    issues = jira.search_issues(
        f'parent in ({epic_string})',
        maxResults=False
    )

    return issues, epic_map, epic_df