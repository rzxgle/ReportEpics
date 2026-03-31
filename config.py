import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

if not all([JIRA_URL, JIRA_EMAIL, JIRA_TOKEN]):
    raise ValueError("Missing environment variables for Jira connection")

EPIC_LINK_FIELD = "customfield_10006"
TEAM_FIELD = "customfield_10001"