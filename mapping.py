import wikipedia
import numpy as np
import matplotlib.pyplot as plt
import time
import operator
from collections import Counter
from serpextract import get_parser, extract, is_serp, get_all_query_params


def map_keywords_to_wikipedia_categories(keywords):
    profile = Counter()
    for keyword in keywords:
        possibilities = wikipedia.search(keyword, results=3, suggestion=False)
        for possibility in possibilities:
            try:
                cats = wikipedia.page(possibility).categories
                if len(cats) > 0:
                    for cat in cats:
                        try:
                            profile[cat] += 1
                        except KeyError, err:
                            profile[cat] = 1
            except:
                'Not Found, do nothing'
    return profile

def extract_params_from_url(ads):
    ads_profile = list()
    for ad in ads:
        serp_url = ad
        ads_profile.extend([get_all_query_params()])
    return ads_profile

def sort_dict(x, n):
    return Counter(dict(x.most_common(n)))

def create_bar_chart(profile, ads_profile):

    profile = sort_dict(profile, 3)
    print profile

    means_profile = profile.values()
    std_profile = profile.keys()

    ads_profile = sort_dict(ads_profile, 3)
    print ads_profile

    means_ads_profile = ads_profile.values()
    std_ads_profile = ads_profile.keys()

    n_groups = 3

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index, means_profile, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_profile,
                 error_kw=error_config,
                 label='User')

    rects2 = plt.bar(index + bar_width, means_ads_profile, bar_width,
                 alpha=opacity,
                 color='g',
                 yerr=std_ads_profile,
                 error_kw=error_config,
                 label='Ads')
    plt.xlabel('Profile')
    plt.ylabel('Abs count')
    plt.title('Count by user and ads')
    plt.xticks(index + bar_width, (profile.keys()))
    plt.legend()

    plt.tight_layout()
    plt.savefig(str(time.strftime("%m%d%y%H%M%S", time.localtime())), bbox_inches='tight')
