import os


def get_fb_credentials(instance):
    instance = "FB_" + instance + "_"
    fb_credentials = {
        "access_token": os.environ[instance + "ACCESSTOKEN"],
        "app_id": os.environ[instance + "APP_ID"],
        "app_secret": os.environ[instance + "APP_SECRET"]
    }
    return fb_credentials
