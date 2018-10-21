from pyfbook.facebook.post import api


def _get_insights(project, post_id, metric, period):
    endpoint = str(post_id) + "/insights"
    params = {
        "metric": metric,
        "period": period
    }
    data = api.get_request(project, post_id, endpoint, params)
    result = {"post_id": post_id, "data": data}
    return result


def insights(project, report_config, period, all_post_id):
    metric = ", ".join(report_config["metric"])
    result = []
    for post_id in all_post_id:
        print("Loading report for post " + str(post_id))
        result.append(_get_insights(project, post_id, metric, period))
    return result

