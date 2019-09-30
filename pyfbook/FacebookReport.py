import yaml
from dbstream import DBStream

from pyfbook.SystemUser import SystemUser
from pyfbook.core.ad_accounts.ad_accounts import process_ad_accounts, get_ad_accounts
from pyfbook.core.marketing.extract.reports.launch import launch
from pyfbook.core.marketing.extract.reports.save import save_reports
from pyfbook.core.marketing.transform_and_load.fetch import check_and_fetch_reports, time_increment_mapping


def launch_reports(facebook, start, end):
    for report in facebook.config["reports"]:
        report_name = report['name']
        for time_increment in report["time_increments"]:
            async_reports = launch(
                facebook=facebook,
                report=report,
                time_increment=time_increment_mapping[time_increment],
                start=start,
                end=end
            )
            save_reports(
                data=async_reports,
                facebook=facebook,
                time_increment=time_increment_mapping[time_increment],
                report_name=report_name
            )


class Facebook:
    def __init__(self, config_path, dbstream: DBStream, launch_jobs=True):
        self.config_path = config_path
        self.config = yaml.load(open(self.config_path), Loader=yaml.FullLoader)
        self.dbstream = dbstream
        self.launch_jobs = launch_jobs

    def get(self, report_name=None, time_increment=None, start=None, end=None, list_account_ids=None):
        if report_name:
            report = list(filter(lambda c: c["name"] == report_name, self.config["reports"]))
            if not report:
                print("No report with this name")
                exit()
            self.config["reports"] = report
        if time_increment:
            for i in range(len(self.config["reports"])):
                self.config["reports"][i]["time_increments"] = [time_increment]
        if list_account_ids:
            for i in range(len(self.config["reports"])):
                self.config["reports"][i]["list_account_ids"] = list_account_ids
        if self.launch_jobs:
            launch_reports(self, start, end)
        bool_ = True
        while bool_:
            bool_ = check_and_fetch_reports(self)

    def get_all_ad_accounts(self):
        table_name = "%s.ad_accounts" % self.config.get("schema_name")
        system_users = SystemUser.all(facebook=self)
        ad_accounts = []
        for system_user in system_users:
            ad_accounts = ad_accounts + get_ad_accounts(system_user)
        process_ad_accounts(ad_accounts, table_name, self)
