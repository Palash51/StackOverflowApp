import time


def get_timestamp(inp_date):
    """convert the datetime to timestamp"""
    timestamp = time.mktime(time.strptime(inp_date, '%Y-%m-%d'))
    return timestamp