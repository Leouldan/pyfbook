import os
import requests
from .. import credentials

DEFAULT_GRAPH_API_VERSION = "v3.0"


def get_request(app_name, endpoint, params):
    api_version = os.environ.get("DEFAULT_GRAPH_API_VERSION")
    if not api_version:
        api_version = DEFAULT_GRAPH_API_VERSION
    fb_credentials = credentials.get_fb_credentials(app_name)
    url = "https://graph.facebook.com/"+api_version+"/" + endpoint
    params["access_token"] = fb_credentials["access_token"]
    data = []
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(r.text)
        raise ValueError("Error when requesting graph api: %s" % r.text)
    result = r.json()
    data = data + result.get("data")
    if result.get("paging"):
        paging = True
        while paging:
            if result["paging"].get("next"):
                r = requests.get(result["paging"]["next"])
                result = r.json()
                data = data + result.get("data")
            else:
                paging = False
    return data
