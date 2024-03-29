import hashlib


def create_id(row, dimension):
    a = ''
    for d in dimension:
        a = a + str(row[d])
    row_id = hashlib.sha224(a.encode()).hexdigest()
    return row_id


def find_purchase_value_in_row(row):
    actions = row.get("actions")
    if actions:
        for item in actions:
            if item["action_type"] == 'offsite_conversion.fb_pixel_purchase':
                purchase_value = item["value"]
                return purchase_value
    else:
        return None


def find_video_view_value(row, action_type):
    actions = row.get("video_10_sec_watched_actions")
    if actions:
        for item in actions:
            if item["action_type"] == action_type:
                value = item["value"]
                return value
    else:
        return None


def compute_total_actions(row):
    actions = row.get("actions")
    total_actions = 0
    if actions:
        for item in actions:
            total_actions = total_actions + int(item["value"])
    return total_actions


def process_data(data, fields, dimension, breakdowns=None):
    all_batch_id = []
    final_data = []
    for row in data:
        final_row = []
        for k in fields:
            if k == "purchase":
                purchase_value = find_purchase_value_in_row(row)
                final_row.append(purchase_value)
            elif k == "total_actions":
                total_actions = compute_total_actions(row)
                final_row.append(total_actions)
            elif k in ("video_view_10_sec",):
                video_view_10_sec = find_video_view_value(row, "video_view")
                final_row.append(video_view_10_sec)
            elif k in row.keys():
                final_row.append(row[k])
            else:
                final_row.append(0)
        if breakdowns:
            for b in breakdowns:
                final_row.append(row[b])
        batch_id = create_id(row, dimension)
        if batch_id not in all_batch_id:
            all_batch_id.append(batch_id)
        final_row.append(batch_id)
        final_data.append(final_row)
    return final_data, all_batch_id


def main(report_config, data):
    columns = report_config["fields"].copy()
    level = report_config["level"]
    if report_config.get("breakdowns"):
        breakdowns = [b for b in report_config.get("breakdowns")]
        dimension = ["account_id", "date_start", "date_stop"] + breakdowns
        columns = columns + breakdowns
    else:
        breakdowns = None
        dimension = ["account_id", "date_start", "date_stop"]
    columns.append("batch_id")
    if level != 'account':
        dimension.append("campaign_id")
        if level != 'campaign':
            dimension.append("adset_id")
            if level != 'adset':
                dimension.append("ad_id")
    fields = report_config["fields"]
    data, all_batch_id = process_data(data, fields, dimension, breakdowns=breakdowns)
    return columns, data, all_batch_id
