#!/usr/bin/env python
import glob
import setuptools
from setuptools import setup
import re


version = re.search("__version__ = '([^']+)'",
                    open('pieisreal/__init__.py').read()).group(1)

setup(
    name="PieIsReal",
    version=version,
    dependency_links=[
        "http://www.pygame.org/ftp/pygame-1.9.1release.tar.gz#egg=pygame-1.9.1"
    ],
    extras_require={'pygame':["pygame>=1.9.2"]},
    description="PieIsReal is a python learning framework forked from"
                " LiveWires. Significantly modified for python 3 compatibility",
    author="Richard Crook, Gareth McCaughan, Paul Wright, Rhodri James,"
           " Neil Turton, Centric Web Estate (Daniel J Holmes)",
    author_email="opensource@centricwebestate.com",
    url="",
    packages=['pieisreal'],
)
