import pyfbook.facebook

all_keys = {
    "marketing": ["account_all_days", "account_day", "campaign_all_days"],
    "page": ["page_all_days", "page_fan"],
    "graph": ["account", "page"]
}


# def api_marketing(app_name, config_path, key, argv):
#     all_account_id = argv
#     for account in all_account_id:
#         result = pyfbook.facebook.marketing.main.main(app_name, config_path, key, account)
#         return result


def get_marketing(project, start, end, all_account_id, spreadsheet_id=None, redshift_instance=None, test=False):
    metric_dimension = pyfbook.facebook.path.get_marketing_metric_dimension(project, test)
    for report_name in metric_dimension.keys():
        report = {
            "name": report_name,
            "config": metric_dimension[report_name]
        }
        print("Loading report %s" % report_name)
        all_time_increment = report["config"]["time_increment"]
        all_result = []
        for time_increment in all_time_increment:
            print("Time increment " + str(time_increment))
            result = pyfbook.facebook.marketing.main.main(project, start, end, report, time_increment, all_account_id,
                                                          redshift_instance, spreadsheet_id)
            all_result.append(result)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None:
            print(all_result)


def get_account_info(project, user_id="me", spreadsheet_id=None, redshift_instance=None, test=False):
    metric_dimension = pyfbook.facebook.path.get_graph_metric_dimension(project, test)
    for report_name in metric_dimension.keys():
        report = {
            "name": report_name,
            "config": metric_dimension[report_name]
        }
        print("Loading report %s" % report_name)
        result = pyfbook.facebook.graph.main.main(project, report, user_id,
                                                  redshift_instance, spreadsheet_id)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None:
            print(result)


#
# def api_graph(key):
#     result = facebook.graph.main.main(key)
#     remove_id(result)
#     pyred.send_to_redshift('MH', result, replace=False)
#
#
# def api_page(key, argv):
#     if len(argv) == 0:
#         all_page_id = facebook.import_redshift.get_all_page_id()
#     else:
#         all_page_id = argv
#     for page in all_page_id:
#         final_result = facebook.page.main.main(key, page)
#         for result in final_result:
#             remove_id(result)
#             pyred.send_to_redshift('MH', result, replace=False)
#
#
# def main(argv):
#     api = argv[0]
#     if api == "graph":
#         key = argv[1]
#         api_graph(key)
#     elif api == "marketing":
#         key = argv[1]
#         try:
#             all_account_id = argv[2:]
#         except:
#             all_account_id = []
#         api_marketing(key, all_account_id)
#     elif api == "page":
#         key = argv[1]
#         try:
#             all_page_id = argv[2:]
#         except:
#             all_page_id = []
#         api_page(key, all_page_id)
#
#
# if __name__ == "__main__":
#     main(sys.argv[1:])
