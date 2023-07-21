from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from fuzzywuzzy import fuzz

import pandas as pd
import os

# -------------------------------------------------------------------
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

# -------------------------------------------------------------------
# Function to calculate the match rate of characters in two strings
def calculate_match(name, email):
    return fuzz.token_sort_ratio(name.lower(), email.lower())

# Initialize variables to keep track of the best match
best_match_rate = 0
best_match_email = ""

# -------------------------------------------------------------------
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
    driver.implicitly_wait(10)
    
    # Find all article titles on the page
    article_titles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "docsum-title", " " ))]')
    
    # Click on the second article title
    article_titles[1].click()
    driver.implicitly_wait(10)

    # Expand author affiliations
    expand_button = driver.find_element('xpath', '//*[(@id = "toggle-authors")]')
    expand_button.click()
    driver.implicitly_wait(10)

    # Find the element containing author affiliations
    author_affiliations = driver.find_element('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "affiliations", " " ))]')

    # Extract the text content of the element
    author_affiliations_text = author_affiliations.text

    # Iterate through each email address and find the one with the highest match rate
    for email_address in author_affiliations_text(". Electronic address: "):
        
        # Extract the name from the email address (everything before the "@")
        name_in_email = email_address.split("@")[0]

        # Calculate the match rate of characters between the name and the email address
        match_rate = calculate_match("Peter G. Szilagyi", name_in_email)

        # Update the best match if the current match rate is higher
        if match_rate > best_match_rate:
            best_match_rate = match_rate
            best_match_email = email_address

        print("Best match email address:", best_match_email)



    




# Wait for the next page to load (you can adjust the time as needed)
driver.implicitly_wait(10)


    

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