import os
import requests
from .. import credentials

DEFAULT_GRAPH_API_VERSION = "v3.3"


def get_request(app_name, endpoint, params):
    api_version = os.environ.get("DEFAULT_GRAPH_API_VERSION")
    if not api_version:
        api_version = DEFAULT_GRAPH_API_VERSION
    fb_credentials = credentials.get_fb_credentials(app_name)
    url = "https://graph.facebook.com/" + api_version + "/" + endpoint
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


def get(system_user, endpoint, params):
    api_version = os.environ.get("DEFAULT_GRAPH_API_VERSION")
    if not api_version:
        api_version = DEFAULT_GRAPH_API_VERSION
    url = "https://graph.facebook.com/%s/%s" % (api_version, endpoint)
    params["access_token"] = system_user.access_token
    data = []
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise ValueError("Error when requesting graph api: %s" % r.text)
    result = r.json()
    if not result.get("data"):
        return []
    data = data + result.get("data")
    paging = True
    c = 0
    while paging:
        c = c + 1
        print(c)
        if result.get("paging"):
            if result["paging"].get("next"):
                r = requests.get(result["paging"]["next"])
                result = r.json()
                if result.get("data"):
                    data = data + result.get("data")
                else:
                    paging = False
            else:
                paging = False
        else:
            paging = False
    return data


def post(system_user, endpoint, params):
    api_version = os.environ.get("DEFAULT_GRAPH_API_VERSION")
    if not api_version:
        api_version = DEFAULT_GRAPH_API_VERSION
    url = "https://graph.facebook.com/%s/%s" % (api_version, endpoint)
    params["access_token"] = system_user.access_token
    r = requests.post(url, params=params)
    if r.status_code != 200:
        raise ValueError("Error when requesting graph api: %s" % r.text)
    result = r.json()
    return result.get('report_run_id')
