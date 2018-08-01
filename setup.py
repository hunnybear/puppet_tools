#!/usr/bin/env python

import setuptools

name = 'puppet_tools'


setuptools.setup(
    name=name,
    version='0.1',
    author="Tyler Jachetta",
    author_email="me@tylerjachetta.net",
    url="tylerjachetta.net",
    description="Utilities for interacting with puppet",
    long_description="todo",
    install_requires=['hb_libs', 'PyYAML'],
    license="GPG version 3",
    packages=setuptools.find_packages(),
    data_files=[],
    entry_points={
        'console_scripts': [
            'puppet_enc=puppet_tools.enc:run',
        ],
    }
)
