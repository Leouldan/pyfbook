import pyfbook.facebook
from pyfbook.facebook.config import get_config
from pyfbook.facebook.date import segment_month_date


def get_marketing(project,
                  start,
                  end,
                  all_account_id,
                  spreadsheet_id=None,
                  redshift_instance=None,
                  test=False,
                  azure_instance=None,
                  prefix_table=None):
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
                                                          redshift_instance, spreadsheet_id, azure_instance,
                                                          prefix_table)
            all_result.append(result)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None and azure_instance is None:
            print(all_result)


def get_account_info(
        project,
        user_id="me",
        spreadsheet_id=None,
        redshift_instance=None,
        test=False,
        azure_instance=None,
        prefix_table=None):
    metric_dimension = pyfbook.facebook.path.get_graph_metric_dimension(project, test)

    for report_name in metric_dimension.keys():
        report = {
            "name": report_name,
            "config": metric_dimension[report_name]
        }
        print("Loading report %s" % report_name)
        result = pyfbook.facebook.graph.main.main(project, report, user_id,
                                                  redshift_instance, spreadsheet_id, azure_instance, prefix_table)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None and azure_instance is None:
            print(result)


def get_page(
        project,
        start,
        end,
        all_page_id,
        spreadsheet_id=None,
        redshift_instance=None,
        test=False,
        azure_instance=None,
        prefix_table=None):
    metric_dimension = pyfbook.facebook.path.get_page_metric_dimension(project, test)

    for report_name in metric_dimension.keys():
        report = {
            "name": report_name,
            "config": metric_dimension[report_name]
        }
        print("Loading report %s" % report_name)
        all_period = report["config"]["period"]
        all_result = []
        for period in all_period:
            print("Period " + str(period))
            all_date = segment_month_date(start, end)
            for date in all_date:
                result = pyfbook.facebook.page.main.main(project, date[0], date[1], report, period, all_page_id,
                                                         redshift_instance, spreadsheet_id, azure_instance,
                                                         prefix_table)
                all_result.append(result)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None and azure_instance is None:
            print(all_result)
            return all_result


def get_post(
        project,
        all_post_id,
        spreadsheet_id=None,
        redshift_instance=None,
        test=False,
        azure_instance=None,
        prefix_table=None):
    metric_dimension = pyfbook.facebook.path.get_post_metric_dimension(project, test)

    for report_name in metric_dimension.keys():
        report = {
            "name": report_name,
            "config": metric_dimension[report_name]
        }
        print("Loading report %s" % report_name)
        all_period = report["config"]["period"]
        all_result = []
        for period in all_period:
            print("Period " + str(period))
            result = pyfbook.facebook.post.main.main(project, report, period, all_post_id,
                                                     redshift_instance, spreadsheet_id, azure_instance,
                                                     prefix_table)
            all_result.append(result)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None and azure_instance is None:
            print(all_result)
            return all_result


def get_page_post(
        project,
        start,
        end,
        page_id,
        spreadsheet_id=None,
        redshift_instance=None,
        test=False,
        azure_instance=None,
        prefix_table=None):
    metric_dimension = pyfbook.facebook.path.get_page_post_metric_dimension(project, test)

    for report_name in metric_dimension.keys():
        report = {
            "name": report_name,
            "config": metric_dimension[report_name]
        }
        print("Loading report %s" % report_name)
        all_result = []
        all_date = segment_month_date(start, end)
        for date in all_date:
            result = pyfbook.facebook.page_post.main.main(project, date[0], date[1], report, page_id,
                                                          redshift_instance, spreadsheet_id, azure_instance,
                                                          prefix_table)
            all_result.append(result)
        print("Finish loading report %s" % report_name)
        if spreadsheet_id is None and redshift_instance is None and azure_instance is None:
            print(all_result)
            return all_result
