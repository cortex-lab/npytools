# -*- coding: utf-8 -*-

"""Tests of core functions."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import numpy as np

from npytools.core import _sizeof, _array_info_table, _tabulate


#------------------------------------------------------------------------------
# Utils
#------------------------------------------------------------------------------

def test_sizeof():
    assert _sizeof(1e24)


def test_array_info_table():
    arr = np.random.rand(10, 10)
    table = _array_info_table(arr, show_stats=True)
    assert table


def test_tabulate():
    assert _tabulate([('a', 1), ('b', 2)])
