#!/usr/bin/env python
"""

Setup script for S3 measurment tool.

"""

import os
import sys
import warnings
from setuptools import setup, Extension, find_packages
from distutils.sysconfig import get_config_vars
from distutils.command import build_ext as build_ext_module
from distutils import ccompiler
from distutils.version import LooseVersion
import argparse
import ctypes
from os.path import join, dirname

from s3measurementset import __version__
