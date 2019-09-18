import logging
import pandas as pd
from pyfbook.facebook.modules.report import launch_report
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
        _send_data(launch_report.main(config, report, time_increment_mapping[time_increment], start, end, async=False),
                   time_increment, report_name, config)
    print("Finish loading report %s" % report_name)


def get_reports(config, start=None, end=None):
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
