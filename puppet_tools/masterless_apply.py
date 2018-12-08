#!/usr/bin/env python
"""
masterless_apply.py

utility for running puppet on nodes directly without having a puppetmaster
around.

TODO:
    *   better exception handling in the subprocess calls, stuff might not
        ~~just~work~~

at home (10.0.0.121 is my laptop at home)

pip install git+ssh://tjachetta@10.0.0.121:~/projects/puppet_tools/puppet_tools

scp 10.0.0.121:~/projects/puppet_tools/puppet_tools/masterless_apply.py . && ./masterless_apply.py

"""

import argparse
import os.path
import subprocess

# Master may require puppet (not puppet-agent) to bootstrap, but I don't know.
REQUIRED_YUM_PACKAGES = ['puppet-agent', 'git']

PUPPET_SRC_URL = "https://github.com/hunnybear/hb_puppet.git"

PUPPET_RELEASE = 'puppetlabs-release-pc1'
REPO_RPMS = {PUPPET_RELEASE: 'https://yum.puppetlabs.com/{0}-el-7.noarch.rpm'.format}

INSTALL_ENV = 'install'


def _get_puppet_path():
    prefix, puppet_path = [s.strip() for s in subprocess.check_output(['whereis', 'puppet']).split(':')]
    assert prefix == 'puppet'
    return puppet_path

def _set_hostname(fqdn):

    cmd = ['hostnamectl', 'set-hostname', fqdn]
    return subprocess.check_call(cmd)


def _parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('hostname')
    parser.add_argument('--role')
    args = parser.parse_args()

    return args


def _setup_packages(packages=REQUIRED_YUM_PACKAGES):

    for name, url in REPO_RPMS.items():
        verify_cmd = ['rpm', '-Vv', name]
        not_present = subprocess.check_call(verify_cmd)

        if not_present:

            repo_cmd = ['rpm', '-Uvh', url]
            subprocess.check_call(repo_cmd)

    cmd = ['yum', '-y', 'install'] + packages
    return subprocess.check_call(cmd)


def _setup_env(environment=INSTALL_ENV):
    puppet = _get_puppet_path()
    cmd = [puppet, 'config', 'print', 'environmentpath']
    environment_root = subprocess.check_output(cmd).strip()

    environment_path = os.path.join(environment_root, environment)
    check_git_cmd = ['git', '--git-dir', environment_path + '/.git',  'status']
    try:
        subprocess.check_call(check_git_cmd)
    except subprocess.CalledProcessError as exc:
        print(check_git_cmd)

        if exc.returncode == 128:
            clone_cmd = ['git', 'clone', '--recursive', PUPPET_SRC_URL, environment_path]
            subprocess.check_call(clone_cmd)

    else:

        pull_cmd = ['git', '--git-dir', environment_path + '/.git', 'pull']
        subprocess.check_call(pull_cmd)


def _do_puppet_run(role, environment=INSTALL_ENV):

    puppet = _get_puppet_path()

    run_cmd = [puppet, 'apply', '--show_diff', '--environment', environment, '-e', 'include role_{0}'.format(role), '--verbose']
    # TODO moar better logging
    print(subprocess.check_output(run_cmd))



def run():

    args = _parse_args()

    _set_hostname(args.hostname)
    _setup_packages()
    _setup_env()
    _do_puppet_run(args.role)


if __name__ == '__main__':
    run()
