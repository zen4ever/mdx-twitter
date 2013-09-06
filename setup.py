#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


from setuptools import setup

import mdx_twitter

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='mdx-twitter',
    version=mdx_twitter.__version__,
    description='Markdown extension for embedding tweets',
    long_description=readme + '\n\n' + history,
    author='Andrii Kurinnyi',
    author_email='andrew@marpasoft.com',
    url='https://github.com/zen4ever/mdx-twitter',
    packages=[
        'mdx_twitter',
    ],
    include_package_data=True,
    install_requires=[
        'Markdown',
        'beautifulsoup4',
        'requests-oauthlib>=0.3.3',
    ],
    tests_require=[
        'httmock',
        'Django>=1.5',
    ],
    license="BSD",
    zip_safe=False,
    keywords='Markdown, Twitter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='runtests.runtests',
)
