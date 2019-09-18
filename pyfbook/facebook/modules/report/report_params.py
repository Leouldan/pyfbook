from pyfbook.facebook.tools.execute_query import execute_query


def prepare_report_request(config, report):
    result = dict()
    result["level"] = report["level"]
    fields = report["fields"].copy()
    if report.get("filtering"):
        result["filtering"] = report.get("filtering")
    if report.get("action_attribution_windows"):
        result["action_attribution_windows"] = report.get("action_attribution_windows")
    if report.get("action_report_time"):
        result["action_report_time"] = report.get("action_report_time")
    if 'account_id' not in fields:
        fields.append('account_id')
    if "purchase" in fields:
        fields[fields.index("purchase")] = "actions"
    elif "total_actions" in fields:
        fields[fields.index("total_actions")] = "actions"
    if "video_view_10_sec" in fields:
        fields[fields.index("video_view_10_sec")] = "video_10_sec_watched_actions"
    if "updated_time" not in fields:
        fields.append("updated_time")
    fields = ", ".join(fields)
    result["fields"] = fields
    if report.get("breakdowns"):
        breakdowns = [b for b in report["breakdowns"]]
        breakdowns = ", ".join(breakdowns)
    else:
        breakdowns = None
    result["breakdowns"] = breakdowns
    if report.get('ad_accounts'):
        accounts = report.get('ad_accounts')
        query = "SELECT DISTINCT id, app_system_user_id, account_id FROM %s WHERE id in ('%s')" % (
            config["schema_name"] + '.ad_accounts', "','".join(accounts))
    else:
        query = 'SELECT DISTINCT id, app_system_user_id, account_id FROM %s' % (config["schema_name"] + '.ad_accounts')
    accounts = execute_query(config=config, query=query)
    result["accounts"] = accounts
    return result
