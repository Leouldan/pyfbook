from . import config_dict
import hashlib
import pandas as pd


def format_dataframe(df):
    result = []
    for i in range(len(df)):
        row = []
        for j in list(df.iloc[i]):
            try:
                if str(j).strip().lower() == "nan":
                    j = 0
            except:
                pass
            if str(type(j)) == "<class 'numpy.int64'>":
                row.append(int(j))
            else:
                row.append(j)

        result.append(row)
    return result


def create_id(row, dimension):
    a = ''
    for d in dimension:
        a = a + str(row[d])
    row_id = hashlib.sha224(a.encode()).hexdigest()
    return row_id


def process_data(page_id, data, metric, dimension, columns):
    frames = []

    dict_items = {item["name"]: data.index(item) for item in data}
    for m in metric:
        if dict_items.get(m) is not None:
            item = data[dict_items[m]]
            df = pd.DataFrame(item["values"])
            df.insert(1, "period", item["period"])
            df.insert(2, "page_id", page_id)
            df = df.rename(columns={"value": item["name"]})
            df = df.fillna(0)
            frames.append(df)
    result = frames[0]
    for k in range(1, len(frames)):
        result = pd.merge(result, frames[k], how='inner', on=dimension)
    for m in metric:
        if m not in list(result.columns):
            result[m] = 0
    result["id"] = result.apply(lambda row: create_id(row, dimension), axis=1)
    result = result[columns]
    final_result = format_dataframe(result)
    return final_result

# def process_data(page_id, data, metric, dimension, columns):
#     frames = []
#     dict_items = {}
#     for item in data:
#         try:
#             dict_items[item["name"]].append(data.index(item))
#         except KeyError:
#             dict_items[item["name"]] = [data.index(item)]
#     for m in metric:
#         if dict_items.get(m) is not None:
#             for j in dict_items[m]:
#                 item = data[j]
#                 df = pd.DataFrame(item["values"])
#                 df.insert(1, "period", item["period"])
#                 df.insert(2, "page_id", page_id)
#                 df = df.rename(columns={"value": item["name"]})
#                 df = df.fillna(0)
#                 frames.append(df)
#
#     # result = frames[0]
#     # for k in range(1, len(frames)):
#     #     result = pd.merge(result, frames[k], how='inner', on=dimension)
#     result = pd.concat(frames)
#     for m in metric:
#         if m not in list(result.columns):
#             result[m] = 0
#     result["id"] = result.apply(lambda row: create_id(row, dimension), axis=1)
#     result = result[columns]
#     final_result = format_dataframe(result)
#     return final_result


def main(key, page_id, data):
    key_config = config_dict.fb_config[key]
    columns = key_config["dimension"].copy() + key_config["metric"].copy()
    columns.append("id")
    dimension = key_config["dimension"]
    metric = key_config["metric"]
    data = process_data(page_id, data, metric, dimension, columns)
    return columns, data
