from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import os

# Set working directory
os.chdir("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/webScraping.R")

# Import Editor-in-Chief names
editor_names = pd.read_csv('scienceDirect_chiefEditor.tsv', sep = '\t')
editor_names = pd.DataFrame(editor_names)

# Set the display options to print the full DataFrame
pd.set_option('display.max_rows', None)  # Print all rows
pd.set_option('display.max_columns', None)  # Print all columns
pd.set_option('display.width', None)  # Print without truncation

print(editor_names['modifiedName'][2])

# Specify the path to the Chromedriver executable
chromedriver_path = 'C:\Program Files\chromedriver_win32\chromedriver.exe'

# Create new instance of the Chrome driver
driver = webdriver.Chrome(executable_path = chromedriver_path)

# Navigate to PubMed
driver.get("https://pubmed.ncbi.nlm.nih.gov/")

# Find search bar element
search_bar = driver.find_element('xpath','//*[(@id = "id_term")]')

# Subset for testing
names_subset = editor_names['modifiedName'][2:3]
print(names_subset)

for name in names_subset:
    print(name)
    
    # Enter the editor's name into the search bar
    search_bar.send_keys(name)
    search_button = driver.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "search-btn", " " ))]')
    search_button.click()
    

    

# for name in editor_names['modifiedName']:
#     print(name)
    
#     # Enter the editor's name into the search bar
#     search_bar.send_keys(editor_names['modifiedName'][1])
#     search_button = driver.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "search-btn", " " ))]')
#     search_button.click()

# Wait for the search results to load
driver.implicitly_wait(10)






# Expand author affiliations
expand_button = driver.find_element('xpath', '//*[(@id = "toggle-authors")]')
expand_button.click()
driver.implicitly_wait(10)

print(editor_names['modifiedName'][1])