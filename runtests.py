#!/usr/bin/env python

import sys
from os.path import abspath, dirname

from django.conf import settings

sys.path.insert(0, abspath(dirname(__file__)))

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.contrib.sessions',
            'tests',
        ),
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        },
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    )


def runtests(modules=['tests']):
    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(failfast=False).run_tests(modules)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
