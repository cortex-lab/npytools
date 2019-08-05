# -*- coding: utf-8 -*-
# flake8: noqa

"""npytools: utilities to deal with NPY files."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import atexit
import logging
import os
import os.path as op
from pathlib import Path
import subprocess
import sys

from io import StringIO

from .core import npyshow


#------------------------------------------------------------------------------
# Global variables and functions
#------------------------------------------------------------------------------

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


def test():  # pragma: no cover
    """Run the full testing suite."""
    import pytest
    pytest.main()
