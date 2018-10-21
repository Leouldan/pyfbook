import os

import yaml

import pyfbook


def get_marketing_metric_dimension(project, test):
    facebook_marketing_yaml_path = os.environ.get("FACEBOOK_MARKETING_%s_YAML_PATH" % project)
    if facebook_marketing_yaml_path:
        print("OK")
        with open(facebook_marketing_yaml_path, 'r') as stream:
            metric_dimension = yaml.load(stream)
        return metric_dimension
    if not facebook_marketing_yaml_path:
        metric_dimension = pyfbook.facebook.marketing.metric_dimension.metric_dimension
        return metric_dimension


def get_page_metric_dimension(project, test):
    facebook_page_yaml_path = os.environ.get("FACEBOOK_PAGE_%s_YAML_PATH" % project)
    if facebook_page_yaml_path:
        with open(facebook_page_yaml_path, 'r') as stream:
            metric_dimension = yaml.load(stream)
        return metric_dimension
    if not facebook_page_yaml_path:
        metric_dimension = pyfbook.facebook.page.metric_dimension.metric_dimension
        return metric_dimension


def get_page_post_metric_dimension(project, test):
    facebook_page_post_yaml_path = os.environ.get("FACEBOOK_PAGE_POST_%s_YAML_PATH" % project)
    if facebook_page_post_yaml_path:
        with open(facebook_page_post_yaml_path, 'r') as stream:
            metric_dimension = yaml.load(stream)
        return metric_dimension
    if not facebook_page_post_yaml_path:
        metric_dimension = pyfbook.facebook.page_post.metric_dimension.metric_dimension
        return metric_dimension


def get_post_metric_dimension(project, test):
    facebook_post_yaml_path = os.environ.get("FACEBOOK_POST_%s_YAML_PATH" % project)
    if facebook_post_yaml_path:
        with open(facebook_post_yaml_path, 'r') as stream:
            metric_dimension = yaml.load(stream)
        return metric_dimension
    if not facebook_post_yaml_path:
        metric_dimension = pyfbook.facebook.post.metric_dimension.metric_dimension
        return metric_dimension


def get_graph_metric_dimension(project, test):
    facebook_graph_yaml_path = os.environ.get("FACEBOOK_GRAPH_%s_YAML_PATH" % project)
    if facebook_graph_yaml_path:
        with open(facebook_graph_yaml_path, 'r') as stream:
            metric_dimension = yaml.load(stream)
        return metric_dimension
    if not facebook_graph_yaml_path:
        metric_dimension = pyfbook.facebook.graph.metric_dimension.metric_dimension
        return metric_dimension
