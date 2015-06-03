from django.dispatch import Signal


done_status_changed = Signal(providing_args=['instance'])
