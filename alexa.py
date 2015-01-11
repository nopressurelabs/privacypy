#
# This is a set of functions to interact with alexa top websites and categories
#

import itertools
import requests
from bs4 import BeautifulSoup

def get_url_list(cat, n):
    """
        Return Alexa first n*25 top sites in one category
        You can provide category as a nested string, ex. cat = "Health"
        or cat = "Health/Mental_Health/Disorders"
        url_list is a list.
    """
    url_list = list()
    i=0
    for _ in itertools.repeat(None, n):
        url = "http://www.alexa.com/topsites/category;" + str(i) + "/Top/" + str(cat)
        i+=1
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        link_list = soup.find_all("li", class_="site-listing")

        for link in link_list:
          url_list.append(link.p.a.text.lower())
    return url_list

def get_top_categories(cats):
    """
    Return Alexa top categories
    cats is a list
    """
    response = requests.get('http://www.alexa.com/topsites/category/Top')
    soup = BeautifulSoup(response.text)
    div_list = soup.find_all("div", class_="categories top")
    ul_list = div_list[0].find_all('ul')
    for ul in ul_list:
        li_list = ul.find_all('li')
        for li in li_list:
            cat = li.a.text[1:-30]
            cats.append(cat)
    return cats

def get_sub_cats(cat):
    """
    Return sub categories given a category cat
    sub_cats is a list
    """

    sub_cats = list()
    url = "http://www.alexa.com/topsites/category/Top/" + str(cat)
    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    ul_list = soup.find_all("span", class_="tr")[0].find_all("div", class_="categories")[0].find_all('ul')
    for ul in ul_list:
        li_list = ul.find_all('li')
        for li in li_list:
            sub_cat = li.a.text[1:-30]
            sub_cats.append(sub_cat)

    return sub_cats
