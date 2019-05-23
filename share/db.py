from django.db.models import Sum
from django.db.models.functions import Coalesce


def sum_zero(*args, **kwargs):
    return Coalesce(Sum(*args, **kwargs), 0)
