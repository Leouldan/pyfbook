import requests
from .. import credentials

APP_NAME = "MHMOET"


def _get_request(endpoint, params):
    fb_credentials = credentials.get_fb_credentials(APP_NAME)
    url = "https://graph.facebook.com/v2.12/" + endpoint
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


def _get_page_access_token(page_id):
    endpoint = "me/accounts"
    params = {"fields": "access_token"}
    data = _get_request(endpoint, params)
    for row in data:
        if row["id"] == page_id:
            return row["access_token"]
    return "Not found"


def get_request(page_id, endpoint, params):
    page_access_token = _get_page_access_token(page_id)
    url = "https://graph.facebook.com/v2.12/" + endpoint
    params["access_token"] = page_access_token
    r = requests.get(url, params=params)
    result = r.json()
    data = result.get("data")
    # if result.get("paging"):
    #     paging = True
    #     while paging:
    #         print(result["paging"])
    #         if result["paging"].get("next"):
    #             r = requests.get(result["paging"]["next"])
    #             result = r.json()
    #             data = data + result.get("data")
    #         else:
    #             paging = False
    return data
