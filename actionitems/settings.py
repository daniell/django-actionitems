from django.conf import settings
from django.db.models import get_model

ORIGIN_MODEL = None  # Setting default to None eases testing
USE_ORIGIN_MODEL = getattr(settings, 'ACTIONITEMS_ORIGIN_MODEL', False)

if USE_ORIGIN_MODEL:
    ORIGIN_MODEL = getattr(settings, 'ACTIONITEMS_ORIGIN_MODEL')

default_manager_list = (('internal', 'Internal'),)
MANAGER_LIST = getattr(settings, 'ACTIONITEMS_MANAGER_LIST', default_manager_list)
