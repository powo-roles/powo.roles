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


def run_playbook_task(click_group, command_name, playbook, decorators=[]):
    host_or_group = 'localhost'
    clickable_ansible.run_playbook_task(
        click_group, command_name,
        playbook, decorators=decorators,
        short_help="Deployment on {}".format(host_or_group),
        help="Deployment on {}".format(host_or_group),
        common_hosts=host_or_group)


def prompt_password(ctx, param, value):
    if value:
        password = click.prompt('Provides a password for user creation',
                                hide_input=True, confirmation_prompt=True)
        ctx.params['password'] = password
        return password


install = run_playbook_task(
    main, 'install', 'playbooks/install.yml',
    decorators=[
        click.option('user', '--user', '-u'),
        click.option('password', '--password', '-p',
                     is_flag=True, callback=prompt_password,
                     expose_value=True),
        click.option('uid', '--uid', '-i'),
        click.option('fullname', '--fullname', '-f'),
        clickable_ansible.kwargs_to_extra_vars('user', 'password', 'uid',
                                               'fullname')
    ])
