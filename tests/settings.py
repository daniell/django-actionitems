import os

USE_TZ = True

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}

RUN_WITH_ORIGIN = os.environ.get('RUN_WITH_ORIGIN', False)  # comes from tox.ini

if RUN_WITH_ORIGIN:
    INSTALLED_APPS = ('actionitems', 'tests')
    ACTIONITEMS_ORIGIN_MODEL = 'tests.TestModel'
else:
    INSTALLED_APPS = ('actionitems',)

ROOT_URLCONF = 'actionitems.urls'

SECRET_KEY = 'ajunksecretkeythatdoesntsecureanything'
