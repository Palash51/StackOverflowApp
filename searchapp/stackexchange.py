from stackauth import StackAuth
from stackexchange import Site, StackOverflow

user_id = '5913966'
STACKOVERFLOW_KEY = 'to6)k4L5p95YPP1adL4PqQ(('


def get_stack_overflow_client():
    """get the stackoverflow client"""
    # site = stackexchange.Site(stackexchange.StackOverflow, app_key=STACKOVERFLOW_KEY)
    so = Site(StackOverflow, STACKOVERFLOW_KEY)
    return so


def get_stackoverflow_user_account(userid):
    """get user account"""
    stack_auth = StackAuth()
    so = get_stack_overflow_client()
    account = stack_auth.associated(so, user_id)
    return account

