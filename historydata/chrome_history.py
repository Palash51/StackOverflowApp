import os
from shutil import copyfile
import sqlite3
from pathlib import Path
# f = open('/home/palash/.config/google-chrome/Default/History', 'r')


src = '/home/palash/.config/google-chrome/Profile 1/History'
dst = '/home/palash/Desktop/palash/Stackexchange/BrowserHistory/browser_data.db'

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
 print(r)