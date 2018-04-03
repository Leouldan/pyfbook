from pyfbook.facebook import date
from pyfbook.facebook.marketing import api


def _get_insights(app_name, account_id, fields, since, until, time_increment, level):
    endpoint = str(account_id) + "/insights"
    time_range = date.since_until_to_time_range(since, until)
    params = {
        "fields": fields,
        "time_range": time_range,
        "level": level,
        "time_increment": time_increment
    }
    data = api.get_request(app_name, endpoint, params)
    return data


def insights(app_name, fb_config, account_id, key):
    key_config = fb_config[key]
    print(key_config)
    level = key_config["level"]
    time_increment = key_config["time_increment"]
    date_window = key_config["date_window"]
    since, until = date.set_since_until(date_window)
    fields = ", ".join(key_config["fields"])
    data = _get_insights(app_name, account_id, fields, since, until, time_increment, level)
    return data

