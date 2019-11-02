# -*- coding: utf-8 -*-

"""Core functions."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import click
import numpy as np
import atexit
import logging
import os
import os.path as op
from pathlib import Path
import subprocess
import sys

from io import StringIO

np.set_printoptions(precision=4, suppress=True, edgeitems=2, threshold=50)


def _git_version():
    """Return the git version."""
    curdir = os.getcwd()
    os.chdir(str(Path(__file__).parent))
    try:
        with open(os.devnull, 'w') as fnull:
            version = ('-git-' + subprocess.check_output(
                       ['git', 'describe', '--abbrev=8', '--dirty', '--always', '--tags'],
                       stderr=fnull).strip().decode('ascii'))
            return version
    except (OSError, subprocess.CalledProcessError):  # pragma: no cover
        return ""
    finally:
        os.chdir(curdir)


__author__ = 'Cyrille Rossant'
__email__ = 'cyrille.rossant at gmail.com'
__version__ = '0.1.0'
__version_git__ = __version__ + _git_version()


# Set a null handler on the root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())
logger.propagate = False


@atexit.register
def on_exit():  # pragma: no cover
    # Close the logging handlers.
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)


#------------------------------------------------------------------------------
# Utils
#------------------------------------------------------------------------------

def _sizeof(num, suffix=''):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1000.0:
            return "%.1f%s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f%s%s" % (num, 'Y', suffix)


def _tabulate(table):
    a = max(len(str(x)) for x, _ in table)
    b = max(len(str(x)) for _, x in table)
    header = '+%s+%s+' % ('-' * (a + 2), '-' * (b + 2))
    table_str = [
        ('| {0: <' + str(a) + '} | {1: <' + str(b) + '} |').format(name, str(value))
        for name, value in table]
    table_str = [header] + table_str + [header]
    return '\n'.join(table_str)


def _array_info_table(arr, show_stats=False):
    size = arr.size
    table = [
        ('shape', arr.shape),
        ('dtype', arr.dtype),
        ('filesize', _sizeof(arr.size * arr.itemsize)),
        ('size', size),
    ]
    if show_stats:
        zero = size - np.count_nonzero(arr)
        table += [
            ('min', arr.min()),
            ('mean', arr.mean()),
            ('median', np.median(arr)),
            ('max', arr.max()),
            ('zero', '%d (%d%%)' % (zero, 100 * float(zero) / size)),
            ('nan', np.isnan(arr).sum()),
            ('inf', np.isinf(arr).sum()),
        ]
    return table


#------------------------------------------------------------------------------
# CLI commands
#------------------------------------------------------------------------------

@click.command('npyshow')
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
@click.option('-n', default=2, help="Number of first/last elements to show.")
@click.option('--show-array/--no-show-array', default=True, help="Whether to show the array.")
@click.option(
    '--show-stats/--no-show-stats', default=False,
    help="Whether to show basic statistics about the array "
    "(requires to load the entire array in memory)")
@click.pass_context
def npyshow(ctx, paths, show_array=True, n=2, show_stats=False):
    """Show array information of a NPY file and possibly display it."""
    np.set_printoptions(edgeitems=n)
    for path in paths:
        if not path.endswith('.npy'):
            continue
        arr = np.load(path, mmap_mode='r')
        table = _array_info_table(arr, show_stats=show_stats)
        click.echo(path)
        click.echo(_tabulate(table))
        if show_array:
            click.echo(arr)
        arr._mmap.close()
