# -*- coding: utf-8 -*-
# flake8: noqa

"""Installation script."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os
import os.path as op
import re

from setuptools import setup, find_packages


#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

curdir = op.dirname(op.realpath(__file__))
with open(op.join(curdir, 'README.md')) as f:
    readme = f.read()


# Find version number from `__init__.py` without executing it.
filename = op.join(curdir, 'npytools.py')
with open(filename, 'r') as f:
    version = re.search(r"__version__ = '([^']+)'", f.read()).group(1)


setup(
    name='npytools',
    version=version,
    license="BSD",
    description='Command-line utilities for the NumPy file format',
    long_description=readme,
    author='Cyrille Rossant (cortex-lab/UCL/IBL)',
    author_email='cyrille.rossant at gmail.com',
    url='https://github.com/cortex-lab/npytools',
    packages=find_packages(),
    package_dir={'npytools': 'npytools'},
    package_data={
        'npytools': [],
    },
    entry_points={
        'console_scripts': [
            'npyshow = npytools:npyshow',
            # 'npyplot = npytools:npyplot',
        ],
    },
    include_package_data=True,
    keywords='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
