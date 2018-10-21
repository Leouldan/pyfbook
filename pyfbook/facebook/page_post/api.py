import os
import requests
from .. import credentials

DEFAULT_GRAPH_API_VERSION = "v3.0"


def _get_request(app_name, endpoint, params):
    api_version = os.environ.get("DEFAULT_GRAPH_API_VERSION")
    if not api_version:
        api_version = DEFAULT_GRAPH_API_VERSION
    fb_credentials = credentials.get_fb_credentials(app_name)
    url = "https://graph.facebook.com/" + api_version + "/" + endpoint
    params["access_token"] = fb_credentials["access_token"]
    data = []
    r = requests.get(url, params=params)
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


def _get_page_access_token(app_name, page_id):
    endpoint = "me/accounts"
    params = {"fields": "access_token"}
    data = _get_request(app_name, endpoint, params)
    for row in data:
        if row["id"] == page_id:
            return row["access_token"]
    return "Not found"


def get_request(app_name, page_id, endpoint, params):
    page_access_token = _get_page_access_token(app_name, page_id)
    api_version = os.environ.get("DEFAULT_GRAPH_API_VERSION")
    if not api_version:
        api_version = DEFAULT_GRAPH_API_VERSION
    url = "https://graph.facebook.com/" + api_version + "/" + endpoint
    params["access_token"] = page_access_token
    r = requests.get(url, params=params)
    if r.status_code != 200:
        print(r.text)
        return []
    result = r.json()
    if not result.get("data"):
        return []
    result = r.json()
    data = result.get("data")
    return data
