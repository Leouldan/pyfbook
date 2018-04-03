from facebook.page import config_dict, api


def _get_insights(page_id, metric, since, until, period):
    endpoint = str(page_id) + "/insights"
    params = {
        "metric": metric,
        "since": since,
        "until": until,
        "period": period
    }
    data = api.get_request(page_id, endpoint, params)
    return data


def insights(page_id, key, since, until):
    key_config = config_dict.fb_config[key]
    period = key_config["period"]
    metric = ", ".join(key_config["metric"])
    data = _get_insights(page_id, metric, since, until, period)
    return data

