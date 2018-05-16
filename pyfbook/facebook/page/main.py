from pyfbook.facebook.page import fetch, process
from pyfbook.facebook import date

from pyfbook.facebook.redshift import to_redshift


def main(project, start, end, report, period, all_page_id,redshift_instance, spreadsheet_id):
    report_name = report.get("name")
    report_config = report.get("config")
    output_storage_name = "facebook.page_" + report_name + "_" + period.replace(":", "_")
    data = fetch.insights(project, start, end, report_config, period, all_page_id)
    columns, data, all_batch_id = process.main(report_config, data)
    result = {
        "table_name": output_storage_name,
        "columns_name": columns,
        "rows": data
    }
    if redshift_instance:  # Send to Redshift
        to_redshift(result, all_batch_id, redshift_instance)
        print(
            "Finished sent to Redshift " + report_name + " " + time_increment + " between " + start + " and " + end)
    if spreadsheet_id:  # Prepare to send to spreadsheet
        result["worksheet_name"] = output_storage_name
    return result

    key_config = config_dict.fb_config[key]
    schema = key_config["schema"]
    table = key_config["table"]
    date_window = key_config["date_window"]
    since, until = date.set_since_until(date_window)
    date_segment = date.segment_month_date(since, until)
    final_result = []
    for row_date in date_segment:
        since = row_date[0]
        until = row_date[1]
        data = fetch.insights(page_id, key, since, until)
        columns, data = process.main(key, page_id, data)
        redshift_table = schema + "." + table
        result = {
            "table_name": redshift_table,
            "columns_name": columns,
            "rows": data
        }
        final_result.append(result)
    return final_result
