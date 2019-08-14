import os
import sys
import django
from django.conf import settings
from shutil import copyfile
import sqlite3
from pathlib import Path

from helpers import get_time_date

sys.path.append("/home/palash/Desktop/palash/Stackexchange/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stackexchange.settings")
django.setup()

# from Stackexchange.middlewares import LoggedInUserMiddleware
# request = LoggedInUserMiddleware(get_response=None)

from history.models import UserHistory


def update_user_history(user):
    """udate user history data"""

    src = '/home/palash/.config/google-chrome/Profile 1/History'
    dst = '/home/palash/Desktop/palash/Stackexchange/Data/browser_data.db'

    try:
        browser_history = open(dst)
    except IOError:
        Path(dst).touch()

    copyfile(src, dst)

    con = sqlite3.connect(dst)
    c = con.cursor()
    query = "select url, title, visit_count, last_visit_time" \
            " from urls " \
            "WHERE url LIKE '%stackoverflow.com/questions%' " \
            "ORDER BY last_visit_time ASC;"

    c.execute(query)
    results = c.fetchall()

    for r in results:
        try:

            user_history = UserHistory.objects.get(
                user=user,
                url=r[0]
            )
        except Exception:
            visit_time = get_time_date(r[3])
            user_history = UserHistory.objects.create(
                user=user,
                url=r[0],
                title=r[1],
                visit_count=r[2],
                last_visit_time=visit_time
            )
    print("updated!!")