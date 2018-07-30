import argparse
import subprocess

import puppet_tools.config

DEFAULT_DOMAIN = 'tylerjachetta.net'

KEY_HIERA_CONFIG = 'hiera_config'


# TODO get prop and module config from config file
PROP_CONFIG = {
    'cluster': None,
    'role': None,
}

MODULE_CONFIG = {}

# Classes

# internal helper functions


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('node_name')

    args = parser.parse_args()

    return args


def _get_hiera_config_path():
    return puppet_tools.config.PuppetConfig().get(KEY_HIERA_CONFIG)


def collect_modules(node_name, config=MODULE_CONFIG):
    # TODO
    pass


def create_props_dict(node_name, config=PROP_CONFIG):
    # TODO
    pass


def run():
    args = _parse_args()

    node_name = args.node_name

    props_dict = create_props_dict(node_name)
    modules = collect_modules(node_name, props_dict)


if __name__ == '__main__':
    run()
