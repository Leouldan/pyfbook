from pyfbook.facebook import date
from pyfbook.facebook.marketing import api


def _get_insights(project, account_id, fields, since, until, time_increment, level):
    endpoint = str(account_id) + "/insights"
    time_range = date.since_until_to_time_range(since, until)
    params = {
        "fields": fields,
        "time_range": time_range,
        "level": level,
        "time_increment": time_increment
    }
    data = api.get_request(project, endpoint, params)
    return data


def insights(project, start, end, report_config, time_increment, all_account_id):
    print(report_config)
    level = report_config["level"]
    fields = ", ".join(report_config["fields"])
    data = []
    for account_id in all_account_id:
        data = data + _get_insights(project, account_id, fields, start, end, time_increment, level)
    return data

