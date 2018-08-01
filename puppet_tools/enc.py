import argparse
import collections

import yaml

import puppet_tools.hiera

DEFAULT_DOMAIN = 'tylerjachetta.net'

_PROPERTY_FIELDS = ('property_name', 'lookup_name', 'required', 'default')
_PROPERTY_DEFAULTS = (None, False, None)

Property = collections.namedtuple(
    'Property', _PROPERTY_FIELDS, defaults=_PROPERTY_DEFAULTS)

# TODO get prop and module config from config file
PROP_CONFIG = [
    Property('role', required=True),
    Property('cluster'),
]

MODULE_CONFIG = []

# Classes

# internal helper functions


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('node_name')

    args = parser.parse_args()

    return args


def collect_modules(node_name, config=MODULE_CONFIG):
    # TODO
    pass


def create_props_dict(node_name, config=PROP_CONFIG):
    props = {}

    for prop in config:
        lookup_name = prop.lookup_name or prop.property_name
        props[prop.property_name] = puppet_tools.hiera.lookup(lookup_name, node=node_name)

    return props

def run():
    args = _parse_args()

    node_name = args.node_name

    props_dict = create_props_dict(node_name)
    modules_dict = collect_modules(node_name, props_dict)

    props_str = yaml.dump(props_dict)
    modules_str = yaml.dump(modules_dict)

    print(props_str)
    print(modules_str)


if __name__ == '__main__':
    run()
