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


def main(fb_config,key, data):
    key_config = fb_config[key]
    columns = key_config["fields"].copy()
    columns.append("id")
    dimension = key_config["dimension"]
    fields = key_config["fields"]
    data = process_data(data, fields, dimension)
    return columns, data
