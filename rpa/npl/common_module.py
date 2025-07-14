from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import time

def initialize_driver():
    options = Options()    
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)    
    options.add_experimental_option('excludeSwitches', ['disable-popup-blocking'])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    return webdriver.Chrome(options=options)
