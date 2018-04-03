from facebook.graph import config_dict, api


def _get_info(endpoint, fields):
    endpoint = "me/"+endpoint
    params = {
        "fields": fields,
    }
    data = api.get_request(endpoint, params)
    return data


def info(key):
    key_config = config_dict.fb_config[key]
    fields = ", ".join(key_config["fields"])
    endpoint = key_config["endpoint"]
    data = _get_info(endpoint, fields)
    return data

