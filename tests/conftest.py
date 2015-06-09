from django import setup
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
setup()
