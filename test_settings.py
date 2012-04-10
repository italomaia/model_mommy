# -*- coding:utf-8 -*-
from os.path import dirname

TEST_ROOT = dirname(__file__)

INSTALLED_APPS = ('model_mommy',)

DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % DATABASE_ENGINE,
        },
    }

SITE_ID = 1
