from pyfbook.facebook.graph import api


def _get_info(project, user_id, endpoint, fields):
    endpoint = str(user_id)+"/"+endpoint
    params = {
        "fields": fields,
    }
    data = api.get_request(project, endpoint, params)
    return data


def info(project, report_config, user_id):
    fields = ", ".join(report_config["fields"])
    endpoint = report_config["endpoint"]
    data = _get_info(project, user_id, endpoint, fields)
    return data

