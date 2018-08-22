import pyodbc
import pyzure


def to_azure(result, all_batch_id, azure_instance):
    all_batch_id = ["'" + e + "'" for e in all_batch_id]
    azure_table = result["table_name"]
    print(azure_table)
    if all_batch_id:
        try:
            query = 'DELETE FROM ' + azure_table + ' WHERE batch_id IN ' + "(" + ",".join(all_batch_id) + ");"
            pyzure.execute.execute_query(azure_instance, query)
        except pyodbc.ProgrammingError:
            pass
    result["columns_name"] = [r.replace(":", "_") for r in result["columns_name"]]
    pyzure.send_to_azure(azure_instance, result, replace=False)
    return 0