import hashlib
import logging

import datetime
import pandas as pd
#import pyzure

from pyfbook.facebook import date
from pyfbook.facebook.date import since_until_to_time_ranges
from pyfbook.facebook.graph.api import get
from pyfbook.facebook.models import SystemUser
from pyfbook.facebook.tools.execute_query import execute_query, send_data

time_increment_mapping = {
    "month": "month",
    "day": "1",
    "week": "week",
    "quarter": "quarter",
    "year": "year",
    "lifetime": "lifetime"
}

SPECIAL_ACTIONS = ["video_10_sec_watched_actions"]


def make_date(date_start, time_increment):
    # if time_increment == 'monthly':
    #     return datetime.datetime.strptime(date_start, '%Y-%m-%d').strftime('%Y-%m-01')
    if time_increment:
        return date_start
    print('Error time increment not specified in make_date function')
    exit()


def make_batch_id(date, account_id):
    return hashlib.sha224((date + str(account_id)).encode()).hexdigest()


def treat_actions(row):
    actions = row.get('actions')
    if actions:
        for action in actions:
            row["action_" + action["action_type"].replace('.', '_')] = action["value"]
        del row['actions']
    return row


def treat_special_action(row, action_name):
    action = row.get(action_name)
    if action:
        row[action_name] = action[0]["value"]
    return row


def _get_insights(config, account, fields, since, until, time_increment, level, breakdowns):
    endpoint = str(account['id']) + "/insights"
    if time_increment in ["week", "month", "quarter", "year"]:
        time_ranges = str(since_until_to_time_ranges(since, until, time_increment))
        params = {
            "fields": fields,
            "time_ranges": time_ranges,
            "level": level,
            "breakdowns": breakdowns
        }
    elif time_increment == 'lifetime':
        params = {
            "fields": fields,
            "level": level,
            "date_preset": 'lifetime',
            "breakdowns": breakdowns
        }
    else:
        time_range = date.since_until_to_time_range(since, until)
        params = {
            "fields": fields,
            "time_range": time_range,
            "level": level,
            "time_increment": time_increment,
            "breakdowns": breakdowns
        }
    data = get(system_user=SystemUser.get(config, account["app_system_user_id"]), endpoint=endpoint, params=params)
    result_data = []
    for row in data:
        row['date'] = make_date(row['date_start'], time_increment)
        row['batch_id'] = make_batch_id(row['date'], row['account_id'])
        row = treat_actions(row)
        for e in SPECIAL_ACTIONS:
            row = treat_special_action(row, action_name=e)
        result_data.append(row)
    return result_data


def get_report_time_increment(config, report, time_increment, start, end):
    level = report["level"]
    fields = report["fields"].copy()
    if 'account_id' not in fields:
        fields.append('account_id')
    if "purchase" in fields:
        fields[fields.index("purchase")] = "actions"
    elif "total_actions" in fields:
        fields[fields.index("total_actions")] = "actions"
    if "video_view_10_sec" in fields:
        fields[fields.index("video_view_10_sec")] = "video_10_sec_watched_actions"
    fields = ", ".join(fields)
    if report.get("breakdowns"):
        breakdowns = [b for b in report["breakdowns"]]
        breakdowns = ", ".join(breakdowns)
    else:
        breakdowns = None
    data = []
    if report.get('ad_accounts'):
        accounts = report.get('ad_accounts')
        query = "SELECT DISTINCT id, app_system_user_id FROM %s WHERE id in ('%s')" % (
            config["schema_name"] + '.ad_accounts', "','".join(accounts))
    else:
        query = 'SELECT DISTINCT id, app_system_user_id FROM %s' % (config["schema_name"] + '.ad_accounts')
    accounts = execute_query(config=config, query=query)
    for account in accounts:
        data = data + _get_insights(config, account, fields, start, end, time_increment, level, breakdowns)
    return data


def _clean_data(config, dict_data, table_name):
    batch_ids = list(set([d['batch_id'] for d in dict_data]))
    query = '''DELETE FROM %s WHERE batch_id in ('%s')''' % (table_name, "','".join(batch_ids))
    try:
        execute_query(config=config, query=query)
    except Exception as e:
        logging.info(str(e))


def _send_data(data, time_increment, report_name, config):
    if not data:
        return 0
    dict_data = pd.io.json.json_normalize(data, sep='__').replace({pd.np.nan: None}).to_dict(
        orient='records')
    columns_name = [c for c in dict_data[0].keys()]
    table_name = '%s.%s_%s' % (config.get('schema_name'), report_name, time_increment)
    _clean_data(config, dict_data, table_name)
    send_data(config=config, data={
        "table_name": table_name,
        "columns_name": columns_name,
        "rows": [[r[c] for c in columns_name] for r in dict_data]
    }, replace=False)


def get_report(config, report, start, end):
    report_name = report['name']
    logging.info("Loading report %s" % report_name)
    time_increments = report["time_increments"]
    for time_increment in time_increments:
        logging.info("Time increment " + str(time_increment))
        _send_data(get_report_time_increment(config, report, time_increment_mapping[time_increment], start, end),
                   time_increment, report_name, config)
    print("Finish loading report %s" % report_name)


def get_reports(config, start, end):
    for report in config.get('reports'):
        get_report(config, report, start, end)


def get_report_history(config, report_name, time_increment=None, start=None, end=None, list_accounts=None):
    for report in config.get('reports'):
        if not report_name == report['name']:
            continue
        if time_increment:
            report['time_increments'] = [time_increment]
        if list_accounts is not None:
            report['ad_accounts'] = list_accounts
        get_report(config, report, start, end)


