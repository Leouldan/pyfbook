import yaml


def get_config(facebookreport):
    try:
        return yaml.load(open(facebookreport.config_path))
    except Exception as e:
        print("Error with config_file: %s" % str(e))
        exit()
