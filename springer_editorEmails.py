from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fuzzywuzzy import fuzz

import os
# import threading
import csv
import concurrent.futures

# -------------------------------------------------------------------
# Set working directory
# This line needs to be run individually (Shift + Enter)
os.chdir("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/webScraping.R")

# -------------------------------------------------------------------
def get_articles(driver):
    return driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')

def accept_cookies(driver):
    try:
        banner_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cc-banner__button-accept", " " ))]')
        banner_button.click()
    except NoSuchElementException: 
        pass

def navigate_and_extract_data(article, driver):
    try:
        journal_name = article.text
        article.click()
        journal_url = driver.current_url
        editor_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "u-list-inline", " " ))]')))
        chief_editor = editor_element.text
        return journal_name, journal_url, chief_editor
    except:
        return None, None, None

def scrape_journal_data(driver, writer):
    articles = get_articles(driver)
    i = 0
    while i < len(articles):
        try:
            accept_cookies(driver)
            article = get_articles(driver)[i]
            
            journal_name, journal_url, chief_editor = navigate_and_extract_data(article, driver)
            
            if journal_name and journal_url and chief_editor:
                writer.writerow([journal_name, journal_url, chief_editor])
            
            driver.back()
            i += 1
        except StaleElementReferenceException:
            print(f"Stale element on article {i}. Refetching articles.")
            articles = get_articles(driver)
        except Exception as e:
            print(f"Error encountered: {e}. Skipping article {i}.")
            i += 1

# -------------------------------------------------------------------
# Specify the path to the Chromedriver executable
chromedriver_path = 'C:\Program Files\chromedriver-win64\chromedriver.exe'

# Create new instance of the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--disable-device-discovery-notifications")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Set timeout to 2 minutes
driver.set_page_load_timeout(120)

# Maximize the browser window to make it fullscreen
driver.maximize_window()

# Extract the names of the Editors-in-Chief and store in TSV
with open('springer_biomedicine.tsv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter="\t")
    writer.writerow(["journalName", "journalURL", "chiefEditor"])

    # Loop through each of the 12 pages
    for page_num in range(1, 13):
        driver.get(f"https://link.springer.com/search/page/{page_num}?facet-discipline=%22Biomedicine%22&facet-content-type=%22Journal%22")
        scrape_journal_data(driver, writer)

# Close the browser
driver.quit()

# -------------------------------------------------------------------

# # Specify the path to the Chromedriver executable
# chromedriver_path = 'C:\Program Files\chromedriver-win64\chromedriver.exe'

# # Create new instance of the Chrome driver
# options = webdriver.ChromeOptions()
# options.add_argument("--disable-device-discovery-notifications")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
# # driver = webdriver.Chrome(executable_path=chromedriver_path)

# # Set timeout to 2 minutes
# # driver.set_page_load_timeout(120)  

# # Maximize the browser window to make it fullscreen
# driver.maximize_window()

# # Initialize TSV file
# with open('springer_biomedicine.tsv', 'w', newline = '', encoding = 'utf-8') as file:
#     writer = csv.writer(file, delimiter = "\t")
#     writer.writerow(["journalName", "journalURL", "chiefEditor"])

#     # Loop through each of the 12 pages
#     for page_num in range(1, 13):
#         driver.get(f"https://link.springer.com/search/page/{page_num}?facet-discipline=%22Biomedicine%22&facet-content-type=%22Journal%22")
        
#         # Get all journal links on the current page
#         articles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')
        
#         # Use an index to loop through articles
#         i = 0
#         while i < len(articles):
#             # Record the current time before navigating to a journal page
#             start_time = time.time()

#             # "Accept cookies" banner
#             try:
#                 try:
#                     banner_button = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cc-banner__button-accept", " " ))]')
#                     banner_button.click()
#                     # Re-fetch the list of articles after closing the banner
#                     articles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')
                
#                 except NoSuchElementException: 
#                     pass  # If the banner button is not found, just continue
                
#                 # Click on the current article using the index
#                 article = articles[i]
#                 journal_name = article.text
                
#                 # Click on the current article using the index
#                 article.click()
                
#                 # Extract journal URL
#                 journal_url = driver.current_url

#                 # Locate the element containing the Editor-in-Chief's name
#                 try:
#                     editor_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "u-list-inline", " " ))]')))
#                     chief_editor = editor_element.text
                
#                 except:
#                     chief_editor = "Not Found"
                
#                 # Write to TSV
#                 writer.writerow([journal_name, journal_url, chief_editor])
                
#                 # Go back to the list of journals
#                 driver.back()
                
#                 # Re-fetch the list of articles after navigating back
#                 articles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]')
                
#                 # Increment the index to process the next article
#                 i += 1

#             except Exception as e:  # Catch all exceptions
#                 print(f"Error encountered: {e}. Skipping current journal.")
#                 i += 1  # Increment the index to process the next article
                
# # Close the browser
# driver.quit()