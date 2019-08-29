import logging

import datetime
import pandas as pd

from pyfbook.facebook.config import get_config
from pyfbook.facebook.graph.api import get as graph_api_get
from pyfbook.facebook.models import SystemUser
from pyfbook.facebook.tools.execute_query import execute_query, send_data


def _clean(all_ids, table_name, config):
    query = 'DELETE FROM %s WHERE id in (%s)' % (table_name, ",".join(all_ids))
    try:
        execute_query(config=config, query=query)
    except Exception as e:
        logging.info(str(e))


def process_campaign(data, table_name, config):
    if not data:
        return 0
    dict_campaign = pd.io.json.json_normalize(data, sep='__').replace({pd.np.nan: None}).to_dict(
        orient='records')
    columns = []
    all_ids = []
    campaigns = []
    for r in dict_campaign:
        all_ids.append(r["id"])
        if r.get("start_time"):
            r["start_time"] = str(datetime.datetime.strptime(r["start_time"][:10], "%Y-%m-%d"))
        if r.get("stop_time"):
            r["stop_time"] = str(datetime.datetime.strptime(r["stop_time"][:10], "%Y-%m-%d"))
        campaigns.append(r)
        for k in r.keys():
            if k not in columns:
                columns.append(k)

    data = {
        "table_name": table_name,
        "columns_name": columns,
        "rows": [[i.get(c) for c in columns] for i in campaigns]
    }

    _clean(all_ids, table_name, config)
    send_data(config=config, data=data, replace=False)


def get_campaigns(account, config, history=False):
    if not history:
        timestamp = str(int(datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(days=7))))
    else:
        timestamp = str(int(datetime.datetime.timestamp(datetime.datetime(2018, 1, 1))))
    filtering = "[{'field': 'campaign.start_time', 'operator': 'GREATER_THAN', 'value': " + timestamp + "}]"

    params = {
        "fields": "account_id,campaign_id,campaign_name,start_time, stop_time, objective",
        "filtering": filtering
    }
    result = graph_api_get(system_user=SystemUser.get(config, account["app_system_user_id"]),
                           endpoint=account["id"] + '/campaigns', params=params)
    return result


def get_all_campaigns(config_path, history=False):
    config = get_config(config_path)
    query = 'SELECT DISTINCT id, app_system_user_id FROM %s' % (config["schema_name"] + '.ad_accounts')
    accounts = execute_query(config=config, query=query)
    data = []
    table_name = "%s.campaigns" % config.get("schema_name")
    for account in accounts:
        data = data + get_campaigns(account, config, history)
    process_campaign(data, table_name, config)
