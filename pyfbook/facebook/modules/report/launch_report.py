import datetime

from pyfbook.facebook.graph.api import post, get
from pyfbook.facebook.models import SystemUser

from pyfbook.facebook.date import since_until_to_time_ranges, since_until_to_time_range
from pyfbook.facebook.modules.report.build_filters import build_active_filter, build_updated_time_filter
from pyfbook.facebook.modules.report.date import define_start_date, define_updated_time_filter
from pyfbook.facebook.modules.report.report_params import prepare_report_request
from pyfbook.facebook.report import treat_actions, SPECIAL_ACTIONS, treat_special_action
from pyfbook.facebook.tools.process_response import make_date, make_batch_id


def _launch_insights(config, account, params, since, until, time_increment, async):
    endpoint = str(account['id']) + "/insights"
    if time_increment in ["week", "month", "quarter", "year"]:
        time_ranges = str(since_until_to_time_ranges(since, until, time_increment))
        params["time_ranges"] = time_ranges
    elif time_increment == 'lifetime':
        params["date_preset"] = 'lifetime'
    else:
        time_range = since_until_to_time_range(since, until)
        params["time_range"] = time_range
    if async:
        data = post(system_user=SystemUser.get(config, account["app_system_user_id"]), endpoint=endpoint, params=params)
        return {'report_run_id': data, 'app_system_user_id': account["app_system_user_id"], 'account_id': account["id"],
                "start_report": since, "end_report": until}
    else:
        data = get(system_user=SystemUser.get(config, account["app_system_user_id"]), endpoint=endpoint, params=params)
        result_data = []
        for row in data:
            row['date'] = make_date(row['date_start'], time_increment)
            row['batch_id'] = make_batch_id(row['date'], account_id=row['account_id'],
                                            campaign_id=row.get("campaign_id"),
                                            adset_id=row.get("adset_id"), ad_id=row.get("ad_id"))
            row = treat_actions(row)
            for e in SPECIAL_ACTIONS:
                row = treat_special_action(row, action_name=e)
            result_data.append(row)
        return result_data


def main(config, report, time_increment, start, end, async):
    r = prepare_report_request(config, report)
    data = []
    for account in r["accounts"]:
        if start is None:
            start = define_start_date(config, report, time_increment, account, async=async)
        if end is None:
            end = str(datetime.datetime.now())[:10]
        if time_increment == 'lifetime':
            updated_time_filter = define_updated_time_filter(config, report, time_increment, account)
            if updated_time_filter:
                updated_time_filter = int(datetime.datetime.timestamp(updated_time_filter))
                r_account = build_active_filter(r)
                data.append(_launch_insights(config, account, r_account, start, end, time_increment, async=async))
                r_account = build_updated_time_filter(r, updated_time_filter)
                data.append(_launch_insights(config, account, r_account, start, end, time_increment, async=async))
            else:
                data.append(_launch_insights(config, account, r, start, end, time_increment, async=async))
        else:
            data.append(_launch_insights(config, account, r, start, end, time_increment, async=async))
    return data
