from pyfbook.facebook.marketing import fetch, process

from pyfbook.facebook.redshift import to_redshift


def main(project, start, end, report, time_increment, all_account_id, redshift_instance, spreadsheet_id):
    report_name = report.get("name")
    report_config = report.get("config")
    output_storage_name = "facebook.marketing_" + report_name + "_" + time_increment.replace(":", "_")
    data = fetch.insights(project, start, end, report_config, time_increment, all_account_id)
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
