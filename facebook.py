#
# Set of functions to interact with Facebook
#

import time
import random
from random import randint

def login(driver, email, password):
    """
        This function need to be passed a Selenium driver to login
        into a facebook account with email and password
    """
    driver.get("http://www.facebook.com/")
    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys(email)
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_id("u_0_n").click()
    time.sleep(randint(5,15))
