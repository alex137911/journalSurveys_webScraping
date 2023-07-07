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

print(editor_names['modifiedName'][0])

# Create new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to PubMed
driver.get("https://pubmed.ncbi.nlm.nih.gov/")

# Find search bar element
search_bar = driver.find_element_by_id("#id_term")
search_bar.send_keys("editor_names['modifiedName'][0]")