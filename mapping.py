import wikipedia
import numpy as np
import matplotlib.pyplot as plt
import time
import operator
from collections import Counter
from serpextract import get_parser, extract, is_serp, get_all_query_params
import requests
from bs4 import BeautifulSoup


def map_keywords_to_wikipedia_categories(keywords, profile):
    for keyword in keywords:
        possibilities = wikipedia.search(keyword, results=5, suggestion=False)
        for possibility in possibilities:
            try:
                cats = wikipedia.page(possibility).categories
                if len(cats) > 0:
                    for cat in cats:
                        dmoz = map_keywords_to_dmoz(cat)
                        if len(dmoz) > 0:
                            for dmoz_cat in dmoz:
                                try:
                                    profile[dmoz_cat] += 1
                                except KeyError, err:
                                    profile[dmoz_cat] = 1
            except:
                'Not Found, do nothing'


def map_keywords_to_dmoz(keyword):
    dmoz_keywords = list()
    url = "http://www.dmoz.org/search?q=" + keyword + "&cat=all&type=ont&all=no&start=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    ol_list = soup.find_all("ol", class_="dir")
    links = ol_list[0].find_all("li")
    for link in links:
        dmoz_keywords.extend([link.a.text.split(':')[0]])
    return dmoz_keywords

def extract_params_from_url(ads):
    ads_profile = list()
    for ad in ads:
        serp_url = ad
        ads_profile.extend([get_all_query_params()])
    return ads_profile

def sort_dict(x, n):
    return Counter(dict(x.most_common(n)))

def create_bar_chart(profile, ads_profile, n_categories, directory):

    means_profile = profile.values()
    std_profile = profile.keys()

    means_ads_profile = ads_profile.values()
    std_ads_profile = ads_profile.keys()

    n_groups = n_categories

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4

    rects1 = plt.bar(index, means_profile, bar_width, alpha=opacity, color='b', label='User')

    rects2 = plt.bar(index + bar_width, means_ads_profile, bar_width, alpha=opacity, color='g', label='Ads')

    plt.xlabel('Profile')
    plt.ylabel('Ads count')
    plt.title('Count by user and ads')
    plt.xticks(index + bar_width, (profile.keys()))
    plt.legend()

    plt.savefig(str(directory + "/" + time.strftime("%m%d%y%H%M%S", time.localtime()) + ".png"))
