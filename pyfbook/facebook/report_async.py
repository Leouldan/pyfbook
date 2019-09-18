import logging

import datetime

import emoji
import os
import pandas as pd
import requests

from pyfbook.facebook.graph.api import get
from pyfbook.facebook.models import SystemUser

from pyfbook.facebook.modules.report import launch_report
from pyfbook.facebook.report import treat_actions, treat_special_action, SPECIAL_ACTIONS, time_increment_mapping
from pyfbook.facebook.tools.execute_query import execute_query, send_data
from pyfbook.facebook.tools.process_response import make_date, make_batch_id

DEFAULT_GRAPH_API_VERSION = "v3.3"


def _clean_data(config, dict_data, table_name):
    report_run_ids = list(set([d['report_run_id'] for d in dict_data]))
    query = '''DELETE FROM %s WHERE report_run_id in ('%s')''' % (table_name, "','".join(report_run_ids))
    try:
        execute_query(config=config, query=query)
    except Exception as e:
        logging.info(str(e))


def save_reports(data, time_increment, report_name, config):
    if not data:
        return 0
    table_name = '%s.%s' % (config.get('schema_name'), 'report_async')
    dict_data = []
    created_at = str(datetime.datetime.now())[:19]
    for r in data:
        r['time_increment'] = time_increment
        r['report_name'] = report_name
        r['status'] = None
        r['result_fetch'] = None
        r['created_at'] = created_at
        r['updated_at'] = created_at
        dict_data.append(r)
    columns_name = [c for c in dict_data[0].keys()]
    _clean_data(config, dict_data, table_name)
    send_data(config=config, data={
        "table_name": table_name,
        "columns_name": columns_name,
        "rows": [[r[c] for c in columns_name] for r in dict_data]
    }, replace=False)


def post_report(config, report, start, end):
    report_name = report['name']
    logging.info("Loading report %s" % report_name)
    time_increments = report["time_increments"]
    for time_increment in time_increments:
        logging.info("Time increment " + str(time_increment))
        save_reports(launch_report.main(config, report, time_increment_mapping[time_increment], start, end, async=True),
                     time_increment=time_increment, report_name=report_name, config=config)
    print("Finish launching async jobs report %s" % report_name)


def post_reports(config, start, end):
    for report in config.get('reports'):
        post_report(config, report, start, end)


def _get_report_status(system_user, endpoint, params):
    api_version = os.environ.get("DEFAULT_GRAPH_API_VERSION")
    if not api_version:
        api_version = DEFAULT_GRAPH_API_VERSION
    url = "https://graph.facebook.com/%s/%s" % (api_version, endpoint)
    params["access_token"] = system_user.access_token
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise ValueError("Error when requesting graph api: %s" % r.text)
    return r.json()


def _clean_data_fetch(config, dict_data, table_name):
    batch_ids = list(set([d['batch_id'] for d in dict_data]))
    query = '''DELETE FROM %s WHERE batch_id in ('%s')''' % (table_name, "','".join(batch_ids))
    try:
        execute_query(config=config, query=query)
    except Exception as e:
        logging.info(str(e))


def extract_emojis(str_):
    return ''.join(c for c in str_ if c in emoji.UNICODE_EMOJI or c in ('🏻', '🇺', '🇸', '🇬', '🇧'))


def replace_all_emoji(str_):
    for i in extract_emojis(str_):
        str_ = str_.replace(i, '???')
    return str_


def _send_data_fetch(data, time_increment, report_name, config):
    if not data:
        return 0
    dict_data = pd.io.json.json_normalize(data, sep='__').replace({pd.np.nan: None}).to_dict(
        orient='records')
    columns_name = [c for c in dict_data[0].keys()]
    table_name = '%s.%s_%s' % (config.get('schema_name'), report_name, time_increment)
    for name in ['campaign_name', 'adset_name', 'ad_name']:
        if name in columns_name:
            for r in dict_data:
                r[name] = replace_all_emoji(r[name])
    _clean_data_fetch(config, dict_data, table_name)
    send_data(config=config, data={
        "table_name": table_name,
        "columns_name": columns_name,
        "rows": [[r[c] for c in columns_name] for r in dict_data]
    }, replace=False)


def _fetch_report(config, r):
    data = get(system_user=SystemUser.get(config, r["app_system_user_id"]),
               endpoint=r['report_run_id'] + '/insights', params={})
    result_data = []
    for row in data:
        row['date'] = make_date(row['date_start'], r["time_increment"])
        row['batch_id'] = make_batch_id(row['date'], account_id=row['account_id'], campaign_id=row.get("campaign_id"),
                                        adset_id=row.get("adset_id"), ad_id=row.get("ad_id"))
        row = treat_actions(row)
        for e in SPECIAL_ACTIONS:
            row = treat_special_action(row, action_name=e)
        result_data.append(row)
    return result_data


def _update_report_status(report, config):
    table_name = '%s.%s' % (config.get('schema_name'), 'report_async')
    updated_at = str(datetime.datetime.now())[:19]

    # noinspection SqlNoDataSourceInspection
    query = '''
              UPDATE %s
              SET updated_at = '%s' ,
              status = '%s', 
              result_fetch = '%s' 
              WHERE report_run_id = '%s' 
    ''' % (
        table_name, updated_at, report["status"], report["result_fetch"], report["report_run_id"])
    execute_query(query, config)


def check_and_fetch_reports(config):
    table_name = '%s.%s' % (config.get('schema_name'), 'report_async')
    all_status = ['Job Completed', 'Job Failed', 'Job Skipped']
    query = '''SELECT * FROM %s WHERE status not in ('%s') or status is NULL or result_fetch is NULL''' % (
        table_name, "','".join(all_status))
    all_reports = execute_query(config=config, query=query)
    job_not_completed_yet = False
    for r in all_reports:
        if r["status"] != 'Job Completed':
            result = _get_report_status(system_user=SystemUser.get(config, r["app_system_user_id"]),
                                        endpoint=r['report_run_id'], params={})
            status = result['async_status']
        else:
            status = r["status"]
        if status == 'Job Completed':
            _send_data_fetch(_fetch_report(config, r), time_increment=r["time_increment"], report_name=r["report_name"],
                             config=config)
            r["result_fetch"] = str(datetime.datetime.now())[:19]
        else:
            job_not_completed_yet = True
            r["result_fetch"] = None
        r["status"] = status
        _update_report_status(r, config)
    return job_not_completed_yet


def get_reports_async(config, start=None, end=None, debug=False):
    """
        config = config file
        start = YYYY-MM-DD
        end = YYYY-MM-DD

        Use asynchronous requests to create insights reports
        Then save these reports in database
        Then check report status and get report result
        End update report status in database
    """
    if not debug:
        post_reports(config, start, end)
    bool_ = True
    while bool_:
        result = check_and_fetch_reports(config)
        if result:
            check_and_fetch_reports(config)
            bool_ = True
        else:
            bool_ = False


def get_report_async_history(config, report_name, time_increment=None, start=None, end=None, list_accounts=None):
    for report in config.get('reports'):
        if not report_name == report['name']:
            continue
        if time_increment:
            report['time_increments'] = [time_increment]
        if list_accounts is not None:
            report['ad_accounts'] = list_accounts
        config['reports'] = [report]
        get_reports_async(config, start, end, debug=False)


def fetch_running_job(config, report_run_id):
    table_name = '%s.%s' % (config.get('schema_name'), 'report_async')
    query = '''SELECT * FROM %s WHERE report_run_id =  '%s' ''' % (table_name, report_run_id)
    r = execute_query(config=config, query=query)[0]

    result = _get_report_status(system_user=SystemUser.get(config, r["app_system_user_id"]),
                                endpoint=r['report_run_id'], params={})
    status = result['async_status']

    if status == 'Job Completed':
        _send_data_fetch(_fetch_report(config, r), time_increment=r["time_increment"], report_name=r["report_name"],
                         config=config)
        r["result_fetch"] = str(datetime.datetime.now())[:19]
    else:
        logging.info('Job not completed yet')
        exit()
    r["status"] = status
    _update_report_status(r, config)
