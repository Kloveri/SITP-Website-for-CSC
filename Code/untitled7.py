# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 14:29:06 2025

@author: DELL
"""
import requests
import json
import time
import random
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery as pq
from selenium import webdriver

driver = webdriver.Edge()
driver.get("https://s.weibo.com/weibo?q=九亭外来&nodup=1&page=1")
time.sleep(3)

driver.quit()
