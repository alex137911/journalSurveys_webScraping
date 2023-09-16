from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fuzzywuzzy import fuzz

import pandas as pd
import time
import os
import re

# -------------------------------------------------------------------
# Set working directory
# This line needs to be run individually (Shift + Enter)
os.chdir("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/webScraping.R")

# -------------------------------------------------------------------
# Function to calculate the match rate of characters in two strings
def calculate_match(name, email):
    return fuzz.token_sort_ratio(name.lower(), email.lower())

# Initialize variables to keep track of the best match
best_match_rate = 0
best_match_email = ""

# Function to relocate the search bar element
# Necessary to prevent stale element reference exception
def find_search_bar():
    while True:
        try:
            return driver.find_element('xpath','//*[(@id = "id_term")]')
        except NoSuchElementException:
            time.sleep(1)  # Wait for 1 second before retrying

# Function to clear the search bar
# search_bar.clear() is not working
def clear_search_bar():
    search_bar = driver.find_element('xpath','//*[(@id = "id_term")]')
    search_bar.send_keys(Keys.CONTROL + "a")  # Select all text in the search bar
    driver.implicitly_wait(10)
    search_bar.send_keys(Keys.DELETE)  # Delete the selected text
    driver.implicitly_wait(10)

# -------------------------------------------------------------------
# Specify the path to the Chromedriver executable
chromedriver_path = 'C:\Program Files\chromedriver-win64\chromedriver.exe'

# Create new instance of the Chrome driver
driver = webdriver.Chrome(executable_path = chromedriver_path)

# Maximize the browser window to make it fullscreen
# Can sometimes help reduce errors from popups blocking elements
driver.maximize_window()
driver.get("https://link.springer.com/search/page/1?facet-discipline=%22Biomedicine%22&facet-content-type=%22Journal%22")
article = driver.find_element('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')
article.click()

# Locate the element containing the Editor-in-Chief's name
editor_element = driver.find_element('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "u-list-inline", " " ))]')

# Extract the name
editor_name = editor_element.text
print(f"Editor-in-Chief: {editor_name}")


