import requests
from .. import credentials


def get_request(app_name, endpoint, params):
    fb_credentials = credentials.get_fb_credentials(app_name)
    url = "https://graph.facebook.com/v2.12/" + endpoint
    params["access_token"] = fb_credentials["access_token"]
    data = []
    r = requests.get(url, params=params)
    result = r.json()
    if not result.get("data"):
        return data
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
