import pyred
# import pyzure


def execute_query(query, config):
    # if config.get('instance').get('type') == 'azure':
    #     return pyzure.execute_query(config.get('instance').get('name'), query)
    if config.get('instance').get('type') == 'redshift':
        return pyred.execute_query(config.get('instance').get('name'), query)


def send_data(data, config, replace=False):
    # if config.get('instance').get('type') == 'azure':
    #     return pyzure.send_data(config.get('instance').get('name'), data, replace=replace)
    if config.get('instance').get('type') == 'redshift':
        return pyred.send_to_redshift(config.get('instance').get('name'), data, replace=replace)
