import json
import os
import sys
import django
from django.conf import settings
from shutil import copyfile
import sqlite3
from pathlib import Path



sys.path.append("/home/palash/Desktop/palash/Stackexchange/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stackexchange.settings")
django.setup()

# from Stackexchange.middlewares import LoggedInUserMiddleware
# request = LoggedInUserMiddleware(get_response=None)

from history.models import UserHistory, BrowsedUrlDetail
from helpers import get_time_date

def update_user_history(user):
    """udate user history data"""

    src = '/home/palash/.config/google-chrome/Profile 1/History'
    dst = '/home/palash/Desktop/palash/Mark-IT/Stackexchange/Data/browser_data.db'

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
    print("updated stackoverflow urls!!")

    all_sites = "select url, title, visit_count, last_visit_time from urls"
    c.execute(all_sites)
    total_sites = c.fetchall()

    for site in total_sites:
        if len(site[0]) < 5000:
            try:

                user_history = BrowsedUrlDetail.objects.get(
                    user=user,
                    site=site[0]
                )
            except Exception:
                visit_time = get_time_date(site[3])
                user_history = BrowsedUrlDetail.objects.create(
                    user=user,
                    site=site[0],
                    site_title=site[1],
                    site_count=site[2],
                    last_visit_time=visit_time
                )

    print("Updated all browsed urls!!")


###################################################



from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from searchapp import models

# Create a connection to ElasticSearch
connections.create_connection()

class MarkedUrlIndex(DocType):
    user = Text()
    url = Text()
    title = Text()
    created_at = Date()


    class Meta:
        index = 'blogpost-index'

# Bulk indexing function, run in shell
# def bulk_indexing():
#     import pdb
#     pdb.set_trace()
#     MarkedUrlIndex.init()
#     es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # actions = [
    #
    #         {"_index": "so-index",
    #             "_type": "question",
    #             "_id": j,
    #              "_source": {
    #                 b.indexing() for b in models.MarkedUrl.objects.all().iterator()
    #             }
    #            for j in range(0, len(models.MarkedUrl.objects.all())
    #         ]
    # bulk(es,actions)

# Simple search function
def search(author):
    s = Search().filter('term', author=author)
    response = s.execute()
    return response


if __name__ == "__main__":

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    select_data = {"created_at": """strftime('%%m/%%d/%%Y', created_at)"""}
    markedurl_data = list(models.MarkedUrl.objects.extra(select=
                                {'created_at':"to_char(created_at, 'YYYY-MM-DD')"}).
                                values('id','user','user__email', 'url', 'title', 'created_at'))
    print(markedurl_data[0])

    for url in markedurl_data:
        es.index(index='marked-ur', doc_type='question', id=url['id'], body=json.dumps(url))

