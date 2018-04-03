from facebook.graph import fetch, process, config_dict


def main(key):
    key_config = config_dict.fb_config[key]
    schema = key_config["schema"]
    table = key_config["table"]
    data = fetch.info(key)
    columns, data = process.main(key, data)
    redshift_table = schema + "." + table
    result = {
        "table_name": redshift_table,
        "columns_name": columns,
        "rows": data
    }
    return result
