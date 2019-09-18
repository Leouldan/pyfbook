import datetime
import logging

from pyfbook.facebook.tools.execute_query import execute_query


# noinspection SqlNoDataSourceInspection
def define_start_date(config, report, time_increment, account, async):
    if async:
        table_name = '%s.%s' % (config.get('schema_name'), 'report_async')
        query = """
                SELECT max(end_report) as start_date
                FROM %s 
                WHERE account_id='%s' and time_increment='%s' and report_name='%s' and status='Job Completed'
                and created_at>=end_report
                """ % (table_name, account["id"], time_increment, report.get('name'))
    else:
        table_name = '%s.%s_%s' % (config.get('schema_name'), report.get('name'), time_increment)
        query = """
                SELECT max(date_start) as start_date
                FROM %s 
                WHERE account_id='%s'
                """ % (table_name, account["account_id"])
    start_date = execute_query(query, config)[0]["start_date"]
    return str(datetime.datetime.strptime(str(start_date)[:10], '%Y-%m-%d') - datetime.timedelta(days=28))[:10]


# noinspection SqlNoDataSourceInspection
def define_updated_time_filter(config, report, time_increment, account):
    table_name = '%s.%s_%s' % (config.get('schema_name'), report.get('name'), time_increment)
    query = """
                SELECT max(updated_time) as updated_time
                FROM %s 
                WHERE account_id='%s'
            """ % (table_name, account["account_id"])
    try:
        updated_time = execute_query(query, config)[0]["updated_time"]
    except Exception as e:
        logging.info(str(e))
        return None
    return datetime.datetime.strptime(str(updated_time)[:10], '%Y-%m-%d') - datetime.timedelta(days=28)
