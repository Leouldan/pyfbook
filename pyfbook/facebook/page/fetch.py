from pyfbook.facebook.page import api


def _get_insights(project, page_id, metric, start, end, period):
    endpoint = str(page_id) + "/insights"
    params = {
        "metric": metric,
        "since": start,
        "until": end,
        "period": period
    }
    data = api.get_request(page_id, endpoint, params)
    return data


def insights(project, start, end, report_config, period, all_page_id):
    metric = ", ".join(report_config["metric"])
    data = []
    for page_id in all_page_id:
        data = _get_insights(project, page_id, metric, start, end, period)
    return data

