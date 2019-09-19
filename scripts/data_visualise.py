import json
import os
import sys
import django
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict, Counter
from pandas.plotting import register_matplotlib_converters

sys.path.append("/home/palash/Desktop/palash/Mark-IT/Stackexchange/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stackexchange.settings")
django.setup()

from history.models import UserHistory, BrowsedUrlDetail

all_months = ['January', 'February', 'March',
              'April', 'May', 'June',
              'July','August', 'September',
              'October', 'November', 'December']

def get_pie_chart():
    count_15 = BrowsedUrlDetail.objects.filter(site_count = 5)
    sites = count_15.values_list('site', flat=True)
    count_count = count_15.values_list('site_count', flat=True)[::1]
    Explode = [0]*len(count_15)
    chart = plt.pie(count_count, explode=Explode, labels=sites, shadow=True, startangle=45)
    plt.axis('equal')
    plt.show()



def get_month_wise_plot():
    all_urls = BrowsedUrlDetail.objects.all()
    user_site_visit_month = [i.last_visit_time.strftime("%B") for i in all_urls]
    mom_user_dict = Counter(user_site_visit_month)
    mom_user = OrderedDict(sorted(mom_user_dict.items(), key=lambda x: all_months.index(x[0])))
    df = pd.DataFrame(list(mom_user.items()), columns=['month', 'total_views'])
    register_matplotlib_converters()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel('Months', fontweight="bold")
    plt.ylabel('Total number of site visits', fontweight="bold")
    ax.set_title('Monthly Plot')
    plt.plot_date(df['month'], df['total_views'], '-o')
    for xy in zip(df['month'], df['total_views']):
        ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data', fontweight="bold")

    # plt.grid()
    plt.show()



def top_three_visited_sites():
    user_url = BrowsedUrlDetail.objects.filter(user=1)
    top_url = user_url.values('site_count', 'site_title')
    final_list = sorted(top_url, key=lambda k: k['site_count'], reverse=True)[:3]
    height = list(map(lambda x: x['site_count'], final_list))
    bars = tuple((map(lambda x: x['site_title'], final_list)))
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height, color=(0.2, 0.4, 0.6, 0.6))
    plt.xticks(y_pos, bars)
    plt.show()



if __name__ == "__main__":
    # top_three_visited_sites()
    get_month_wise_plot()
    # get_pie_chart()





# def main():
#     # Make an example pie plot
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#
#     labels = ['Beans', 'Squash', 'Corn']
#     wedges, plt_labels = ax.pie([20, 40, 60], labels=labels)
#     ax.axis('equal')
#
#     make_picker(fig, wedges)
#     plt.show()

# def make_picker(fig, wedges):
#     import webbrowser
#     def on_pick(event):
#         wedge = event.artist
#         label = wedge.get_label()
#         webbrowser.open('http://images.google.com/images?q={0}'.format(label))
#
#     # Make wedges selectable
#     for wedge in wedges:
#         wedge.set_picker(True)
#
#     fig.canvas.mpl_connect('pick_event', on_pick)
#
# if __name__ == '__main__':
#     main()