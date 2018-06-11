from pyfbook.facebook.page import api


def _get_insights(project, page_id, metric, start, end, period):
    endpoint = str(page_id) + "/insights"
    params = {
        "metric": metric,
        "since": start,
        "until": end,
        "period": period
    }
    data = api.get_request(project, page_id, endpoint, params)
    result = {"page_id": page_id, "data": data}
    return result


def insights(project, start, end, report_config, period, all_page_id):
    metric = ", ".join(report_config["metric"])
    result = []
    for page_id in all_page_id:
        print("Loading report for page " + str(page_id))
        result.append(_get_insights(project, page_id, metric, start, end, period))
    return result
