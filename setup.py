#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='mdx-twitter',
    version='0.1.0',
    description='Markdown extension for embedding tweets',
    long_description=readme + '\n\n' + history,
    author='Andrii Kurinnyi',
    author_email='andrew@marpasoft.com',
    url='https://github.com/zen4ever/mdx-twitter',
    packages=[
        'mdx_twitter',
    ],
    package_dir={'mdx_twitter': 'mdx_twitter'},
    include_package_data=True,
    install_requires=[
        'Markdown',
        'requests-oauthlib>=0.3.3',
    ],
    license="BSD",
    zip_safe=False,
    keywords='mdx-twitter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)