from pyfbook.facebook.azure import to_azure
from pyfbook.facebook.post import fetch, process

from pyfbook.facebook.redshift import to_redshift


def main(
        project,
        report,
        period,
        all_post_id,
        redshift_instance,
        spreadsheet_id,
        azure_instance,
        prefix_table):
    report_name = report.get("name")
    report_config = report.get("config")
    output_storage_name = "facebook.post_" + report_name + "_" + period.replace(":", "_")
    data = fetch.insights(project, report_config, period, all_post_id)
    columns, data, all_batch_id = process.main(report_config, data)

    result = {
        "table_name": output_storage_name,
        "columns_name": columns,
        "rows": data
    }

    if prefix_table:
        result["table_name"] = prefix_table + "_" + result["table_name"]

    if redshift_instance:  # Send to Redshift
        to_redshift(result, all_batch_id, redshift_instance)
        print(
            "Finished sent to Redshift " + report_name + " " + period)

    if azure_instance:  # Send to Azure
        to_azure(result, all_batch_id, azure_instance)
        print(
            "Finished sent to Azure " + report_name + " " + period)

    if spreadsheet_id:  # Prepare to send to spreadsheet
        result["worksheet_name"] = output_storage_name
    return result


