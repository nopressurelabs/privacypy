#
# This is a set of functions to browse websites
#
import time
import os
import random
import urllib, urllister
import mapping
from collections import Counter
from random import randint
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import pickle # to load and save cookies

def create_browser_driver(browser,extensions):
    """
        Browser is a string specifying the browser time
        extensions is a list of extensions

    """
    if browser == 'Firefox':
        fp = webdriver.FirefoxProfile()
        for ext in extensions:
            fp.add_extension(extension=ext)
        driver = webdriver.Firefox(firefox_profile=fp)
        return driver

def save_ads_links(driver, directory, timestamp):
    """
        Save ads link from a page
        Pretty raw
    """
    frames = driver.find_elements_by_tag_name("iframe")
    file_name = directory + "/" + timestamp + "-ads-source.log"
    f = open(file_name,'w')
    for frame in frames:
        driver.switch_to.frame(frame)
        try:
            a = driver.find_element_by_tag_name('a')
            f.write(a.get_attribute('innerHTML').encode('utf-8'))
            f.write(a.get_attribute('href').encode('utf-8'))
        except Exception:
            f.write(driver.page_source.encode('utf-8'))
        driver.switch_to.default_content()
    f.close

def get_ads_links(driver):
    """
        Get ads links from page
    """
    ads = list()
    frames = driver.find_elements_by_tag_name("iframe")
    if len(frames)>0:
        for frame in frames:
            driver.switch_to.frame(frame)
            try:
                a = driver.find_element_by_tag_name('a')
                ads.extend([a.get_attribute('innerHTML')])
                ads.extend([a.get_attribute('href')])
            except Exception:
                scripts = driver.find_elements_by_tag_name("iframe")
                for script in scripts:
                    driver.switch_to.frame(script)
                    try:
                        ads.extend([script.get_attribute('src')])
                    except Exception:
                        'Do nothing, not found'
                    driver.switch_to.default_content()
                    driver.switch_to.frame(frame)
            driver.switch_to.default_content()
    return ads

def save_headers(driver, directory, timestamp):
    """
        Save headers and meta stuff from a page
        Pretty raw
    """
    headers = driver.find_elements_by_tag_name("meta")
    file_name = directory + "/" + timestamp + "-meta-source.log"
    f = open(file_name,'w')
    for header in headers:
        f.write(header.get_attribute('outerHTML').encode('utf-8'))
    f.close

def get_header_keywords(driver):
    """
        return a list of keywords given a Selenium driver
    """
    keywords = list()
    headers = driver.find_elements_by_tag_name("meta")
    for header in headers:
        if header.get_attribute('name') == 'keywords':
            keywords.extend(header.get_attribute('content').split(','))
    return keywords

def random_elem(elems):
    """
        Return random element
    """
    indices = random.sample(range(len(elems)), 1)
    sample_elem = [elems[i] for i in sorted(indices)][0]
    return sample_elem

def links_in_page(page_url,tag):
    """
        Given a html document and a tag, return all tag objects.
    """
    usock = urllib.urlopen(page_url)
    parser = urllister.URLLister()
    parser.feed(usock.read())
    usock.close()
    parser.close()
    return parser.urls

def visit_list(url_list, driver, ads, keywords):
    """
        Visit URL list and dump stuff
    """
    current_time = str(time.strftime("%m%d%y%H%M%S", time.localtime()))
    directory = 'session' + str(current_time)
    profile = Counter()
    ads_profile = Counter()

    if not os.path.exists(directory):
        os.makedirs(directory)
        os.makedirs(directory + "/cookies")

    # if os.path.isfile("cookies/cookies.pkl"):
    #     cookies = pickle.load(open("cookies/cookies.pkl", "rb"))
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)

    for url in url_list:
        time.sleep(randint(5,15))
        n = 1 # randint(2,9)
        driver.get(url) # load page
        screenshot = directory + "/" + str(time.strftime("%m%d%y%H%M%S", time.localtime())) + ".png"
        driver.get_screenshot_as_file(screenshot)
        source_dir = directory + "/" + str(time.strftime("%m%d%y%H%M%S", time.localtime())) + "-source.log"
        f = open(source_dir,'w')
        f.write(driver.page_source.encode('utf-8'))
        keywords.extend(get_header_keywords(driver))
        ads.extend(get_ads_links(driver))
        if len(keywords) > 0:
            profile = mapping.map_keywords_to_wikipedia_categories(keywords)
        if len(ads) > 0:
            ads_tags = list()
            ads_tags = mapping.extract_params_from_url(ads)
            ads_profile = mapping.map_keywords_to_wikipedia_categories(ads_tags)
        if len(ads)>0 and len(keywords)>0:
            mapping.create_bar_chart(profile, ads_profile)
        i=0
        while i < n:
            links = driver.find_elements_by_tag_name('a')
            if links:
                link = random_elem(links)
                driver.get(link.get_attribute("href")) # get individual 1,2,3,4 pages
                time.sleep(randint(25,35))
                timestamp = str(time.strftime("%m%d%y%H%M%S", time.localtime()))
                screenshot = directory + "/" + timestamp + ".png"
                driver.get_screenshot_as_file(screenshot)
                source_dir = directory + "/" + timestamp + "-source.log"
                f = open(source_dir,'w')
                f.write(driver.page_source.encode('utf-8'))
                save_ads_links(driver, directory, timestamp)
                save_headers(driver, directory, timestamp)
                keywords.extend(get_header_keywords(driver))
                ads.extend(get_ads_links(driver))
                if len(keywords) > 0:
                    profile = mapping.map_keywords_to_wikipedia_categories(keywords)
                if len(ads) > 0:
                    ads_tags = list()
                    ads_tags = mapping.extract_params_from_url(ads)
                    ads_profile = mapping.map_keywords_to_wikipedia_categories(ads_tags)
                if len(ads)>0 and len(keywords)>0:
                    mapping.create_bar_chart(profile, ads_profile)
                driver.back() # return to page that has 1,2,3,next -like links
                time.sleep(randint(5,15))
                i +=1
            else:
                break
    # Write cookies to load later
    pickle.dump( driver.get_cookies() , open("cookies/cookies.pkl","wb"))

    # Write cookies to file
    file_dir = directory + "/cookies/cookies.log"
    f = open(file_dir,'w')
    cookies = driver.get_cookies()
    f.write(cookies) # python will convert \n to os.linesep
    f.close()
    return [ads, keywords]
