import os

import yaml


def get_marketing_metric_dimension(project, test):
    facebook_marketing_yaml_path = os.environ.get("FACEBOOK_MARKETING_%s_YAML_PATH" % project)
    if test and not facebook_marketing_yaml_path:
        facebook_marketing_yaml_path = "pyfbook/facebook/marketing/metric_dimension.yaml"
    elif not facebook_marketing_yaml_path:
        print("No GOOGLE_ANALYTICS_YAML_PATH configured")
        exit()
    with open(facebook_marketing_yaml_path, 'r') as stream:
        metric_dimension = yaml.load(stream)
    return metric_dimension

