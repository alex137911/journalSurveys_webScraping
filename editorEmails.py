from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from fuzzywuzzy import fuzz

import pandas as pd
import os
import re

# -------------------------------------------------------------------
# Set working directory
# This line needs to be run individually (Shift + Enter)
os.chdir("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/webScraping.R")

# Import Editor-in-Chief names
editor_names = pd.read_csv('scienceDirect_chiefEditor.tsv', sep = '\t')
editor_names = pd.DataFrame(editor_names)

# Set the display options to print the full DataFrame
pd.set_option('display.max_rows', None)  # Print all rows
pd.set_option('display.max_columns', None)  # Print all columns
pd.set_option('display.width', None)  # Print without truncation

# print(editor_names['modifiedName'][2])

# Initialize empty column to hold email addresses
editor_names['editorEmail'] = None

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
# names_subset = editor_names['modifiedName'][2:3]
# print(names_subset)

for name in editor_names['modifiedName']:
    print(name)
    
    # Enter the editor's name into the search bar
    search_bar.send_keys(name)
    search_button = driver.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "search-btn", " " ))]')
    search_button.click()
    driver.implicitly_wait(10)
    
    # Find all article titles on the page
    article_titles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "docsum-title", " " ))]')
    num_articles = min(len(article_titles), 10)

    # Loop through first 10 articles (or the number of articles if less than 10)
    for i in range(num_articles):
        # Fetch the titles again for the next iteration
        article_titles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "docsum-title", " " ))]')
        
        # Click on article title
        article_titles[i].click()
        driver.implicitly_wait(10)

        # Expand author affiliations to find emails (if possible, otherwise skip article)
        try:
            expand_button = driver.find_element('xpath', '//*[(@id = "toggle-authors")]')
            expand_button.click()
            driver.implicitly_wait(10)

            # Find the element containing author affiliations
            author_affiliations = driver.find_element('xpath', '//*[contains(concat( " ", @class, " " ), concat( " ", "affiliations", " " ))]')

            # Extract the text content of the element
            author_affiliations_text = author_affiliations.text

            # Use regular expressions to extract email addresses (i.e. text containing "@")
            email_pattern = re.compile(r"[^\s]+@[^\s]+")
            email_addresses = re.findall(email_pattern, author_affiliations_text)

            # Check if email_addresses is empty
            if not email_addresses:
                print("No email address found for:", name)
                # Skip to the next article
                driver.back()
                continue

            # Initialize list to store email addresses containing best match
            email_match = []

            # Loop through the email addresses to find those associated with "Peter G. Szilagyi"
            for email in email_addresses:
                # Extract the name from the email address (everything before the "@")
                name_in_email = email.split("@")[0].strip()
                print(name_in_email)

                # Calculate the match rate of characters between the name and the email address
                match_rate = calculate_match(name, name_in_email)
                print(match_rate)

                # Update the best match if the current match rate is higher
                if match_rate > best_match_rate:
                    best_match_rate = match_rate
                    best_match_email = email

            # Print the email address
            print("Email addresses for Editor-in-Chief:", best_match_email)

            # Add the email address to the DataFrame
            editor_names.loc[editor_names['modifiedName'] == name, 'editorEmail'] = str(best_match_email)

            # Go back to the search results page
            driver.back()
            
        except NoSuchElementException:
            print(f"Author affiliations not found for article {i + 1}. Skipping to the next article.")
            # Go back to the search results page
            driver.back()
            continue