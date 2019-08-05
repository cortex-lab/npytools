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
    header = '+%s|%s+' % ('-' * (a + 2), '-' * (b + 2))
    table_str = [
        ('| {0: <' + str(a) + '} | {1: <' + str(b) + '} |').format(name, str(value))
        for name, value in table]
    table_str = [header] + table_str + [header]
    return '\n'.join(table_str)


def _array_info_table(arr):
    size = arr.size
    table = [
        ('shape', arr.shape),
        ('dtype', arr.dtype),
        ('filesize', _sizeof(arr.size * arr.itemsize)),
        ('size', size),
        ('zero', size - np.count_nonzero(arr)),
        ('nan', np.isnan(arr).sum()),
        ('inf', np.isinf(arr).sum()),
    ]
    return table


#------------------------------------------------------------------------------
# CLI commands
#------------------------------------------------------------------------------

@click.command('npyshow')
@click.argument('path', type=click.Path(exists=True))
@click.pass_context
def npyshow(ctx, path):
    """Describe a NPY file."""
    arr = np.load(path, mmap_mode='r')
    table = _array_info_table(arr)
    click.echo(_tabulate(table))
    click.echo(arr)
