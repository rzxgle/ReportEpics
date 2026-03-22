import streamlit as st
from jira import JIRA
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
        fields=["summary"]
    )

    epic_map = {epic.key: epic.fields.summary for epic in epics}

    epic_keys = list(epic_map.keys())

    if not epic_keys:
        return [], {}

    epic_string = ",".join(epic_keys)

    issues = jira.search_issues(
        f'parent in ({epic_string}) AND status not in (Inválido, Cancelado)',
        maxResults=False
    )

    return issues, epic_map