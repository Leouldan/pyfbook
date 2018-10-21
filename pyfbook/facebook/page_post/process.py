import hashlib


def create_id(row, dimension):
    a = ''
    for d in dimension:
        a = a + str(row[d])
    row_id = hashlib.sha224(a.encode()).hexdigest()
    return row_id


def process_data(data, fields, dimension):
    all_batch_id = []
    final_data = []
    for row in data:
        final_row = []
        for k in fields:
            if k == 'message':
                k = k[:75]
            if k in row.keys():
                final_row.append(row[k])
            else:
                final_row.append(0)
        batch_id = create_id(row, dimension)
        if batch_id not in all_batch_id:
            all_batch_id.append(batch_id)
        final_row.append(batch_id)
        final_data.append(final_row)
    return final_data, all_batch_id


def main(report_config, data):
    columns = report_config["fields"].copy()
    columns.append("batch_id")
    all_dimension = ["id"]
    dimension = [item for item in all_dimension if item in report_config["fields"]]
    fields = report_config["fields"].copy()
    data, all_batch_id = process_data(data, fields, dimension)
    return columns, data, all_batch_id
