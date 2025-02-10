#! /usr/bin/env python
from __future__ import print_function  # pylint: disable=unused-import

import logging
import os.path
import pprint
import sys

import click

from ruamel.yaml import YAML
 
import clickable
from clickable.utils import PathResolver
from clickable.coloredlogs import bootstrap


bootstrap()
logger = logging.getLogger('clickable')
stdout = logging.getLogger('stdout.{}'.format(clickable.__name__))


@click.group()
@click.pass_context
def cli(ctx):
    path_resolver = PathResolver(sys.modules[__name__])
    ctx.obj['path_resolver'] = path_resolver
    ctx.obj['project_root'] = \
        os.path.normpath(os.path.dirname(sys.modules[__name__].__file__))
    conf_path = os.path.join(ctx.obj['project_root'], 'clickable.yaml')
    if os.path.isfile(conf_path):
        with open(conf_path) as f:
            yaml = YAML(typ='safe')
            configuration = yaml.load(f)
            ctx.obj.update(configuration)
    logger.info('loaded configuration: \n{}'.format(pprint.pformat(ctx.obj)))


@cli.command()
@click.pass_context
def molecule(ctx):
    """
    Symlink molecule/*/molecule.yml files to molecule/default/molecule.yml
    """
    path = os.path.normpath(os.path.join(ctx.obj['project_root'], 'molecule'))
    default = os.path.normpath(os.path.join(
        ctx.obj['project_root'], 'molecule', 'default', 'molecule.yml'
    ))
    logger.debug("using {} as target for molecule.yml links".format(default))
    logger.debug("scanning {}".format(path))
    failed = False
    for folder_basename in os.listdir(path):
        m_folder = os.path.join(path, folder_basename)
        if os.path.isdir(m_folder) and os.path.basename(m_folder) != 'default':
            target = os.path.normpath(os.path.join(
                m_folder, 'molecule.yml'
            ))
            logger.debug("checking {}".format(target))
            if os.path.exists(target):
                if not os.path.islink(target):
                    stdout.warn("{} already exists and is not replaced".format(target))
                    failed = True
                    continue
                if not os.path.samefile(target, default):
                    stdout.warn("{} is symlink but does not target {}".format(target, default))
                    failed = True
                    continue
                stdout.info("{} symlink already exists".format(target))
            else:
                stdout.info("{} created as {} symlink".format(target, default))
                os.symlink(os.path.relpath(default, os.path.dirname(target)), target)
    if failed:
        stdout.error("some molecule.yml links cannot be created")
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
