# -*- coding: utf-8 -*-

"""Core functions."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import click
import numpy as np

np.set_printoptions(precision=4, suppress=True, edgeitems=2, threshold=50)


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
@click.argument('path', type=click.Path(exists=True))
@click.option('-n', default=2, help="Number of first/last elements to show.")
@click.option('--show-array/--no-show-array', default=True, help="Whether to show the array.")
@click.option(
    '--show-stats/--no-show-stats', default=False,
    help="Whether to show basic statistics about the array "
    "(requires to load the entire array in memory)")
@click.pass_context
def npyshow(ctx, path, show_array=True, n=2, show_stats=False):
    """Show array information of a NPY file and possibly display it."""
    np.set_printoptions(edgeitems=n)
    arr = np.load(path, mmap_mode='r')
    table = _array_info_table(arr, show_stats=show_stats)
    click.echo(path)
    click.echo(_tabulate(table))
    if show_array:
        click.echo(arr)
