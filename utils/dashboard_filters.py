def get_available_teams(team_progress):
    return sorted(team_progress["team"].dropna().unique())


def filter_by_teams(epic_progress, team_progress, selected_teams):
    filtered_epic_progress = epic_progress[
        epic_progress["team"].isin(selected_teams)
    ]

    filtered_team_progress = team_progress[
        team_progress["team"].isin(selected_teams)
    ]

    return filtered_epic_progress, filtered_team_progress