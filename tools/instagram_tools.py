try:
    import os
    import re
    import sys
    import json
    import time
    import logging
    import datetime
    import argparse
    import requests
    import configparser
    from enum import Enum
    from time import sleep
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from datetime import datetime, timedelta
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.support import expected_conditions as EC
except ImportError as exception:
    print("%s - Please install the necessary libraries." % exception)
    sys.exit(1)


def get_instagram_posts(username):
    """
    Get users info from config file and get users info and followers size.
    Args:
        username - instagram user name.
    Returns:
        ---
    """
    posts_information = {}
    posts_information.setdefault('instagram', [])

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_experimental_option("prefs", {"download.default_directory": os.getcwd()})

    browser = webdriver.Chrome(chrome_options=chrome_options)
    # makes sure slower connections work as well
    browser.implicitly_wait(10)

    try:
        # Get url from config file.
        url = 'https://www.instagram.com/' + username

        browser.get(url)

        timeout = 1
        try:
            element_present = EC.presence_of_element_located((By.ID, 'main'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")
        browser.execute_script("return window.location.href")

        print ('Get posts from user feed')
        post_urls = browser.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")
        for url in post_urls:
            each_post_info = {}
            each_post_info['username'] = username
            each_post_info['url'] = url.find_element_by_tag_name('a').get_attribute('href')
            each_post_info['image'] = url.find_element_by_xpath("//div[@class='KL4Bh']/img").get_attribute('src')
            each_post_info['publishedAt'] = ''
            #response = requests.get('https://api.instagram.com/oembed?url=' + each_post_url).json()
            posts_information['instagram'].append(each_post_info)

    except KeyboardInterrupt:
        print ('Aborted...')

    finally:
        browser.delete_all_cookies()
        browser.close()
    return posts_information
