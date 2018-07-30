"""
hiera.py

utilities and such for interacting specifically with hiera.

This was developed with hiera 3.4.3 and it looks like migration changes should
be pretty minor, but just getting that in here so that if I start seeing issues
I can remember that maybe something changed.
"""

import subprocess

LOOKUP_ARG_NODE = '--node'


def lookup(*keys, node=None, compile_puppet=True):
    """ Returns a puppet lookup [Hiera lookup].

    Does a puppet lookup (which used to be accessed via hiera lookup) command
    and returns the results.

    Keyword Arg:
        node: Name of the node to lookup. If None provided, will look up this
            node.
        compile_puppet: set this to False if you know that puppet has been
            compiled on the target node since the node's hiera data has
            changed. This should really only be set to False if you're running
            lookup twice (and not changing hiera data in between), and only on
            the second run.

    Author:
        * Tyler Jachetta, me@tylerjachetta.net
    """

    cmd = ['puppet', 'lookup']

    if node is not None:
        cmd += [LOOKUP_ARG_NODE, node]

    cmd += keys

    return subprocess.check_output(cmd)
