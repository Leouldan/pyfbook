time_increment_mapping = {
    "month": "month",
    "day": "1",
    "week": "week",
    "quarter": "quarter",
    "year": "year",
    "lifetime": "lifetime"
}
SPECIAL_ACTIONS = ["video_10_sec_watched_actions"]


def treat_actions(row):
    actions = row.get('actions')
    if actions:
        for action in actions:
            row["action_" + action["action_type"].replace('.', '_')] = action["value"]
        del row['actions']
    return row


def treat_special_action(row, action_name):
    action = row.get(action_name)
    if action:
        row[action_name] = action[0]["value"]
    return row
