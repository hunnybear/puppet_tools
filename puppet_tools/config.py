"""
puppet_tools/config.py

Utility classes and functions for interacting with puppet configs.
"""

import subprocess

PUPPET_CONFIG_OUT_DELIM = ' = '

MSG_MALFORMED_LINE = 'unrecognized format for puppet config output: {0}'


class PuppetConfig(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PuppetConfig, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._all_items = {}

        self._fetch()

    def _fetch(self):

        cmd = ['puppet', 'config', 'print']
        raw_out = subprocess.check_output(cmd)

        new_vals = {}

        for line in raw_out.splitlines():
            if not line.strip():
                continue

            if PUPPET_CONFIG_OUT_DELIM not in line:
                # TODO better logging
                print(MSG_MALFORMED_LINE.format(line))

            key, val = [item.strip() for item in line.split(PUPPET_CONFIG_OUT_DELIM, 1)]
            new_vals[key] = val

        self._all_items = new_vals

    def get(self, key):
        # TODO put in some timeout for fetching values
        # TODO might want to wrap the keyerror here and give it a gussied up
        # exception, but then again might not.
        return self._all_items[key]
