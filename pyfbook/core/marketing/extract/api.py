import os

import requests

API_VERSION = os.environ.get("DEFAULT_GRAPH_API_VERSION") if os.environ.get("DEFAULT_GRAPH_API_VERSION") else " v3.3"
BASE_URL = "https://graph.facebook.com/%s/%s"

def post(system_user, endpoint, params):
    url = BASE_URL % (API_VERSION, endpoint)
    params["access_token"] = system_user.access_token
    r = requests.post(url, params=params)
    if r.status_code != 200:
        raise ValueError("Error when requesting graph api: %s" % r.text)
    result = r.json()
    return result.get('report_run_id')


def get_report_status(system_user, endpoint, params):
    url = BASE_URL % (API_VERSION, endpoint)
    params["access_token"] = system_user.access_token
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise ValueError("Error when requesting graph api: %s" % r.text)
    return r.json()


def get(system_user, endpoint, params):
    url = BASE_URL % (API_VERSION, endpoint)
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
        print("Paging: " + str(c))
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
