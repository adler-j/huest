"""Setup script for huest.

Installation command::

    pip install [--user] [-e] .
"""

from __future__ import print_function, absolute_import

from setuptools import setup, find_packages

setup(
    name='huest',

    version='0.0.0',

    description='HoUnsfield ESTimate',

    url='https://github.com/adler-j/huest',

    author='Jonas Adler',

    license='GPLv3+',

    keywords='research development emission prototyping imaging tomography',

    packages=find_packages(exclude=['*test*']),
    package_dir={'huest': 'huest'},

    install_requires=['numpy']
)
