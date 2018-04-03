from facebook.page import fetch, process, config_dict
from facebook import date


def main(key, page_id="330188133767801"):
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
