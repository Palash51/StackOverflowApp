import time
from datetime import datetime, timedelta
from django.core.cache import cache
from rest_framework.authtoken.models import Token

from searchapp.models import User


def get_timestamp(inp_date):
    """convert the datetime to timestamp"""
    timestamp = time.mktime(time.strptime(inp_date, '%Y-%m-%d'))
    return timestamp


def get_time_date(inp_timestamp):
    """convert the timestamp to datetime"""
    epoch_start = datetime(1601, 1, 1)
    delta = timedelta(microseconds=int(inp_timestamp))
    return epoch_start + delta


def get_logged_user():
    """get the user using cache token"""
    user_token = cache.get("SE_token")
    print(user_token)
    user_id = Token.objects.get(key=user_token).user_id
    user = User.objects.get(id=user_id)
    return user