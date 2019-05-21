#! /bin/env python
# -*- encoding: utf-8 -*-
from __future__ import print_function

import logging

import click

import clickable.utils
import clickable.coloredlogs

import clickable_ansible


# bootstrap logging system
clickable.coloredlogs.bootstrap()
logger = logging.getLogger('stdout.clickable')


# name consistently with click-infra entry point
@click.group()
@click.pass_context
def main(ctx):
    """
    Deployment or development tasks
    """
    clickable.utils.load_config(ctx, __name__, __file__, 'clickables.yml')


def run_playbook_task(click_group, command_name, playbook, host_or_group):
    clickable_ansible.run_playbook_task(click_group, command_name,
        playbook, short_help="Deployment on {}".format(host_or_group),
        help="Deployment on {}".format(host_or_group),
        common_hosts=host_or_group)

install = run_playbook_task(main, 'install', 'playbooks/install.yml', "localhost")
