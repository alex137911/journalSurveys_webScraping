from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fuzzywuzzy import fuzz

import csv
import pandas as pd
import time
import os
import re

# -------------------------------------------------------------------
# Set working directory
# This line needs to be run individually (Shift + Enter)
os.chdir("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/webScraping.R")

# -------------------------------------------------------------------
# Specify the path to the Chromedriver executable
chromedriver_path = 'C:\Program Files\chromedriver-win64\chromedriver.exe'

# Create new instance of the Chrome driver
driver = webdriver.Chrome(executable_path=chromedriver_path)

# Maximize the browser window to make it fullscreen
driver.maximize_window()

# Initialize CSV file
with open('springer_biomedicine.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["journalName", "journalURL", "chiefEditor"])

    # Loop through each of the 12 pages
    for page_num in range(1, 13):
        driver.get(f"https://link.springer.com/search/page/{page_num}?facet-discipline=%22Biomedicine%22&facet-content-type=%22Journal%22")
        
        # Get all journal links on the current page
        articles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')
        
        for article in articles:
            # Extract journal name
            journal_name = article.text
            
            # Click on the journal link
            article.click()
            
            # Extract journal URL
            journal_url = driver.current_url
            
            # Locate the element containing the Editor-in-Chief's name
            try:
                editor_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "u-list-inline", " " ))]')))
                chief_editor = editor_element.text
            except:
                chief_editor = "Not Found"
            
            # Write to CSV
            writer.writerow([journal_name, journal_url, chief_editor])
            
            # Go back to the list of journals
            driver.back()

# Close the browser
driver.quit()

# -------------------------------------------------------------------
# # Specify the path to the Chromedriver executable
# chromedriver_path = 'C:\Program Files\chromedriver-win64\chromedriver.exe'

# # Create new instance of the Chrome driver
# driver = webdriver.Chrome(executable_path = chromedriver_path)

# # Maximize the browser window to make it fullscreen
# # Can sometimes help reduce errors from popups blocking elements
# driver.maximize_window()
# driver.get("https://link.springer.com/search/page/1?facet-discipline=%22Biomedicine%22&facet-content-type=%22Journal%22")
# article = driver.find_element('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')
# article.click()

# # Locate the element containing the Editor-in-Chief's name
# editor_element = driver.find_element('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "u-list-inline", " " ))]')

# # Extract the name
# editor_name = editor_element.text
# print(f"Editor-in-Chief: {editor_name}")


