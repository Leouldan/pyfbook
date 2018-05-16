from pyfbook.facebook import date
from pyfbook.facebook.marketing import api


def _get_insights(project, account_id, fields, since, until, time_increment, level, breakdowns):
    endpoint = str(account_id) + "/insights"
    time_range = date.since_until_to_time_range(since, until)
    params = {
        "fields": fields,
        "time_range": time_range,
        "level": level,
        "time_increment": time_increment,
        "breakdowns": breakdowns
    }
    data = api.get_request(project, endpoint, params)
    return data


def insights(project, start, end, report_config, time_increment, all_account_id):
    level = report_config["level"]
    fields = report_config["fields"].copy()
    if "purchase" in fields:
        fields[fields.index("purchase")] = "actions"
    fields = ", ".join(fields)
    if report_config.get("breakdowns"):
        breakdowns = [b for b in report_config.get("breakdowns")]
        breakdowns = ", ".join(breakdowns)
    else:
        breakdowns = None
    data = []
    for account_id in all_account_id:
        data = data + _get_insights(project, account_id, fields, start, end, time_increment, level, breakdowns)
    return data

