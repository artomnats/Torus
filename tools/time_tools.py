try:
    import sys
    import pytz
    from dateutil import parser
    from datetime import datetime
    from django.utils import timezone
    from pytz.exceptions import UnknownTimeZoneError
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(0)

# -- For unit tests - -----------------------------------------------------------------------------
_fixed_time_now = None  # used in unit tests only


def set_fixed_time_now(t):
    global _fixed_time_now
    _fixed_time_now = t


def time_now():
    return _fixed_time_now or timezone.now()


def list_time_zones():
    return pytz.all_timezones
