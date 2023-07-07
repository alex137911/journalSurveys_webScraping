from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

import pandas as pd

# Create new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to PubMed