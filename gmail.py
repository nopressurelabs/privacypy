#
# Set of functions to interact with Gmail
#

import time
import random
from random import randint

def login(driver, email, password):
    """
        This function need to be passed a Selenium driver to login
        into a gmail account with email and password
    """
    driver.get("http://mail.google.com")
    emailid=driver.find_element_by_id("Email")
    emailid.send_keys(email)
    passw=driver.find_element_by_id("Passwd")
    passw.send_keys(password)
    signin=driver.find_element_by_id("signIn")
    signin.click()
    time.sleep(randint(5,15))
