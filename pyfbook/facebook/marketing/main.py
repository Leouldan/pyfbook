from pyfbook.facebook.marketing import fetch, process, config_dict


def main(app_name, config_path, key, account_id):
    fb_config = config_dict.yaml_to_dict(config_path)
    key_config = fb_config[key]
    schema = key_config["schema"]
    table = key_config["table"]
    data = fetch.insights(app_name, fb_config, account_id, key)
    columns, data = process.main(fb_config, key, data)
    redshift_table = schema + "." + table
    result = {
        "table_name": redshift_table,
        "columns_name": columns,
        "rows": data
    }
    return result
