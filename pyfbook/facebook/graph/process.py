from . import config_dict
import hashlib


def create_id(row, dimension):
    a = ''
    for d in dimension:
        a = a + str(row[d])
    row_id = hashlib.sha224(a.encode()).hexdigest()
    return row_id


def process_data(data, fields, dimension):
    final_data = []
    for row in data:
        final_row = []
        for k in fields:
            if k in row.keys():
                final_row.append(row[k])
            else:
                final_row.append(0)
        final_row.append(create_id(row, dimension))
        final_data.append(final_row)
    return final_data


def process_data_page(data, fields):
    final_data = []
    for row in data:
        final_row = []
        for k in fields:
            if k in row.keys():
                final_row.append(row[k])
            else:
                final_row.append(0)
        final_data.append(final_row)
    return final_data


def main(key, data):
    key_config = config_dict.fb_config[key]
    columns = key_config["fields"].copy()
    if key == "page":
        fields = key_config["fields"]
        data = process_data_page(data, fields)
        return columns, data
    columns.append("id")
    dimension = key_config["dimension"]
    fields = key_config["fields"]
    data = process_data(data, fields, dimension)
    return columns, data
