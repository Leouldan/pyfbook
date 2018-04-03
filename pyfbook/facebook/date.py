import datetime
import json

DATE_FORMAT = "%Y-%m-%d"


def date_to_string(date):
    return date.strftime(DATE_FORMAT)


def string_to_date(string):
    return datetime.datetime.strptime(string, DATE_FORMAT)


def segment_month_date(start, end):
    """
    start : YYYY-MM-DD
    end : YYYY-MM-DD
    """
    start_datetime = string_to_date(start)
    end_datetime = string_to_date(end)
    result = []

    while start_datetime.replace(day=1) != end_datetime.replace(day=1):
        inter = [date_to_string(start_datetime + datetime.timedelta(days=-1)),
                 date_to_string(end_of_month(start_datetime) + datetime.timedelta(days=1))]
        result.append(inter)
        start_datetime = add_a_month(start_datetime)
    result.append([date_to_string(start_datetime + datetime.timedelta(days=-1)),
                   date_to_string(end_datetime + datetime.timedelta(days=1))])
    return result


def add_a_month(date):
    try:
        nextmonthdate = date.replace(month=date.month + 1, day=1)
    except ValueError:
        if date.month == 12:
            nextmonthdate = date.replace(year=date.year + 1, month=1, day=1)
        else:
            # next month is too short to have "same date"
            # pick your own heuristic, or re-raise the exception:
            raise
    return nextmonthdate


def remove_a_month(date):
    try:
        previousmonthdate = date.replace(month=date.month - 1, day=1)
    except ValueError:
        if date.month == 1:
            previousmonthdate = date.replace(year=date.year - 1, month=12, day=1)
        else:
            # next month is too short to have "same date"
            # pick your own heuristic, or re-raise the exception:
            raise
    return previousmonthdate


def end_of_month(date):
    return add_a_month(date) + datetime.timedelta(days=-1)


def define_date(year, month):
    since = datetime.date(year, month, 1).strftime(DATE_FORMAT)
    until = datetime.date.today().strftime(DATE_FORMAT)
    return since, until


def define_date_year(year):
    since = datetime.date(year, 1, 1)
    until = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    since = since.strftime(DATE_FORMAT)
    until = until.strftime(DATE_FORMAT)
    return since, until


def since_until_to_time_range(since, until):
    time_range = {
        "since": since,
        "until": until
    }
    time_range = json.dumps(time_range)
    return time_range


def set_last_year():
    last_year = datetime.date.today().year
    return define_date_year(last_year)


def set_default():
    return define_date(2018, 1)


def set_lifetime():
    return define_date(2017, 1)


def set_since_until(date_window):
    try:
        since = date_window["since"]
        until = date_window["until"]
    except TypeError or AttributeError:
        function_to_run = globals()["set_" + date_window]
        since, until = function_to_run()
    return since, until
