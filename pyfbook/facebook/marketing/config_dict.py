import yaml


def yaml_to_dict(path_file):
    with open(path_file, 'r') as stream:
        fb_config = yaml.load(stream)
    return fb_config
