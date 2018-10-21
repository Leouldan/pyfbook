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


def process_data(post_id, data, metric, dimension, columns):
    frames = []

    dict_items = {item["name"]: data.index(item) for item in data}
    for m in metric:
        if dict_items.get(m) is not None:
            item = data[dict_items[m]]
            df = pd.DataFrame(item["values"])
            df.insert(1, "period", item["period"])
            df.insert(2, "post_id", post_id)
            df = df.rename(columns={"value": item["name"]})
            df = df.fillna(0)
            frames.append(df)
    result = frames[0]
    for k in range(1, len(frames)):
        result = pd.merge(result, frames[k], how='inner', on=dimension)
    for m in metric:
        if m not in list(result.columns):
            result[m] = 0
    result["post_id"] = post_id
    result["batch_id"] = result.apply(lambda row: create_id(row, dimension), axis=1)
    all_batch_id = list(result["batch_id"])
    result = result[columns]
    final_result = format_dataframe(result)
    return final_result, all_batch_id


def main(report_config, data):
    columns = report_config["metric"].copy()
    dimension = ["post_id"]
    columns.append("post_id")
    columns.append("period")
    columns.append("batch_id")
    metric = report_config["metric"].copy()
    data_process = []
    all_batch_id = []
    for rawdata in data:
        post_id = rawdata["post_id"]
        print("Process data for post " + str(post_id))
        data_one_post = rawdata["data"]
        if data_one_post:
            data_one_post, all_batch_id_one_post = process_data(post_id, data_one_post, metric, dimension, columns)
            data_process = data_process + data_one_post
            all_batch_id = all_batch_id + all_batch_id_one_post
    return columns, data_process, all_batch_id
