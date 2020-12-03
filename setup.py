###############################################################################
#
# Copyright 2017 by Plone Foundation and Shoobx, Inc.
#
###############################################################################
"""Shoobx JUnit XML Setup
"""
import sys
from setuptools import setup, find_packages


setup(
    name='shoobx.junitxml',
    version='0.2.2.dev0',
    description=
        'A zope.testrunner output formatter & feature to output JUnit XML.',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='jenkins junit xml zope.testing',
    author='Shoobx, Inc. and Martin Aspelli',
    author_email='dev@shoobx.com',
    url='http://pypi.python.org/pypi/shoobx.junitxml',
    license='ZPL 2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'lxml',
        'setuptools',
        'zope.testrunner',
    ],
    test_suite='shoobx.junitxml',
)
