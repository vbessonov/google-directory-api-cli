"""CLI mm robot interface made with Click
"""
import logging.config
import sys

import click
from gcp.directory.cli import directory


def excepthook(exc_type, exc_value, exc_traceback):
    logging.fatal(f'Exception hook has been fired: {exc_value}', exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = excepthook


@click.group()
@click.option('--config', '-c', help='Path to the configuration file', default='config.yml')
@click.option('--logging-config', '-l', help='Path to the logging configuration file', default='logging.yml')
@click.pass_context
def cli(*args, **kwargs):
    pass


cli.add_command(directory)
