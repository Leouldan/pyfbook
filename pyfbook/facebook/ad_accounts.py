import logging

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


def process_ad_accounts(ad_accounts, table_name, config):
    if not ad_accounts:
        return 0
    dict_ad_accounts = pd.io.json.json_normalize(ad_accounts, sep='__').replace({pd.np.nan:None}).to_dict(orient='records')
    columns = []
    all_ids = []
    unique_ad_accounts = []
    for r in dict_ad_accounts:
        if r["id"] in all_ids:
            continue
        all_ids.append(r["id"])
        unique_ad_accounts.append(r)
        for k in r.keys():
            if k not in columns:
                columns.append(k)

    data = {
        "table_name": table_name,
        "columns_name": columns,
        "rows": [[i.get(c) for c in columns] for i in unique_ad_accounts]
    }

    _clean(all_ids, table_name, config)
    send_data(config=config, data=data, replace=False)


def get_ad_accounts(system_user):
    params = {
        "fields": "name,account_id,currency,business,partner,owner,user_role"
    }
    result = graph_api_get(system_user, "me/adaccounts", params)
    for r in result:
        r["app_system_user_id"] = system_user.id
    return result


def get_all_ad_accounts(config_path):
    config = get_config(config_path)
    table_name = "%s.ad_accounts" % config.get("schema_name")
    system_users = SystemUser.all(config)
    ad_accounts = []
    for system_user in system_users:
        ad_accounts = ad_accounts + get_ad_accounts(system_user)
    process_ad_accounts(ad_accounts, table_name, config)
