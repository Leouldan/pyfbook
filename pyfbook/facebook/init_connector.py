from pyfbook.facebook.tools.execute_query import send_data


def main(config, params):
    table_name = "%s.app_system_user" % config.get("schema_name")
    columns_name = ["id", "app_id_name", "app_secret_name", "access_token_name"]
    data = {
        "table_name": table_name,
        "columns_name": columns_name,
        "rows": [[params.get(c) for c in columns_name]]
    }
    send_data(data, config, replace=False)
