#!/usr/bin/env python

import glob
from setuptools import setup
import re


version = re.search("__version__ = '([^']+)'",
                    open('livewires/__init__.py').read()).group(1)

setup (name = "LiveWires",
       version = version,
       install_requires = ['pygame'],
       description = "LiveWires package provides resources for people learning Python. It is intended for use with the LiveWires Python Course",
       author = "Richard Crook, Gareth McCaughan, Paul Wright, Rhodri James, Neil Turton",
       author_email = "python@livewires.org.uk",
       url = "http://www.livewires.org.uk/python/",
       packages = ['livewires'],
      )

