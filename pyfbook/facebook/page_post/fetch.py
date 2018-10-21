from pyfbook.facebook.page_post import api


def insights(project, report_config, since, until, page_id):
    fields = ", ".join(report_config["fields"])
    print("Fetching all post from page " + str(page_id))
    endpoint = str(page_id) + "/posts"
    params = {
        "fields": fields,
        "since": since,
        "until": until

    }
    data = api.get_request(project, page_id, endpoint, params)
    return data
