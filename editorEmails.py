from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from fuzzywuzzy import fuzz

import pandas as pd
import time
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

# Initialize empty column to hold match score (higher score is better)
editor_names['confidenceScore'] = None

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
chromedriver_path = 'C:\Program Files\chromedriver_win32\chromedriver.exe'

# Create new instance of the Chrome driver
driver = webdriver.Chrome(executable_path = chromedriver_path)

# Maximize the browser window to make it fullscreen
# Can sometimes help reduce errors from popups blocking elements
driver.maximize_window()

# Navigate to PubMed
driver.get("https://pubmed.ncbi.nlm.nih.gov/")

# Find search bar element
search_bar = driver.find_element('xpath','//*[(@id = "id_term")]')

# Subset for testing
# indexes_to_select = [7, 11, 25, 29, 39, 44, 50, 57, 61, 75, 79, 89, 94, 100, 107, 111, 125, 129, 139, 144]
# names_subset = editor_names.loc[indexes_to_select, 'modifiedName']
# names_subset = editor_names['modifiedName'][7]
# print(names_subset)

# editor_names['modifiedName']

start_time = time.time()

for name in editor_names['modifiedName']:
    print(name)

    # Reset the best match variables
    best_match_rate = 0
    best_match_email = ""
    
    # Clear the search bar for the next iteration
    search_bar = find_search_bar()
    clear_search_bar()

    # Enter the editor's name into the search bar
    search_bar.send_keys(name)
    search_button = driver.find_element('xpath','//*[contains(concat( " ", @class, " " ), concat( " ", "search-btn", " " ))]')
    
    # search_button.click()
    driver.execute_script("arguments[0].click();", search_button)
    driver.implicitly_wait(10)

    # Check to see if query landed on search page (to deal with edge case where zero/one article is found)
    try:
        search_results = driver.find_element('xpath','//*[(@id = "search-results")]')

        # Find all article titles on the page
        article_titles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "docsum-title", " " ))]')
        num_articles = min(len(article_titles), 10)

        # Loop through first 10 articles (or the number of articles if less than 10)
        for i in range(num_articles):
            # Fetch the titles again for the next iteration
            article_titles = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "docsum-title", " " ))]')
            
            # Scroll the element (i.e., the journal article) into view
            # Necessary to prevent popups from blocking the element ("intercepts" the click)
            driver.execute_script("arguments[0].scrollIntoView();", article_titles[i])
           
            # Click on article title
            # article_titles[i].click()
            driver.execute_script("arguments[0].click();", article_titles[i])
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

                # Loop through the email addresses
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

                # Check if the best match rate is 100
                if best_match_rate == 100:
                    print("Email address for Editor-in-Chief:", best_match_email)
                    print("Perfect match found. Skipping remaining articles.")

                    # Add the email address to the DataFrame
                    editor_names.loc[editor_names['modifiedName'] == name, 'editorEmail'] = str(best_match_email)
                    
                    # Add the match rate to the DataFrame
                    editor_names.loc[editor_names['modifiedName'] == name, 'confidenceScore'] = best_match_rate
                    break  # Exit the loop

                # Print the email address
                print("Email address for Editor-in-Chief:", best_match_email)

                # Add the email address to the DataFrame
                editor_names.loc[editor_names['modifiedName'] == name, 'editorEmail'] = str(best_match_email)

                # Add the match rate to the DataFrame
                editor_names.loc[editor_names['modifiedName'] == name, 'confidenceScore'] = best_match_rate

                # Go back to the search results page
                driver.back()
                driver.implicitly_wait(10)
                
            # If the author affiliations are not found, skip to the next article     
            except NoSuchElementException:
                print(f"Author affiliations not found for article {i + 1}. Skipping to the next article.")
                # Go back to the search results page
                driver.back()
                driver.implicitly_wait(10)
                continue

    except NoSuchElementException:
        print(f"Search result for editor {name} failed. Skipping to the next editor.")

        # Navigate back to PubMed
        driver.get("https://pubmed.ncbi.nlm.nih.gov/")
        
        # Find search bar element
        search_bar = driver.find_element('xpath','//*[(@id = "id_term")]')
        
        # Clear the search bar for the next iteration
        search_bar.clear()
        continue

# Calculate and print the runtime
end_time = time.time()
runtime = end_time - start_time
print(f"Total runtime: {runtime:.2f} seconds")

# Close the browser
driver.close()

# -------------------------------------------------------------------
# Remove characters not part of email address (e.g., "." at the end of string)
# editor_names['editorEmail'] = editor_names['editorEmail'].str.replace(r'\.[^.]*$', '', regex = True)
editor_names['editorEmail'] = editor_names['editorEmail'].str.replace(r'\.$', '', regex = True)

# Create direcotry to store output
if not os.path.exists("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/editorEmails.py"):
    os.mkdir("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/editorEmails.py")

# Save the DataFrame as a .csv file to directory
editor_names.to_csv("C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data/editorEmails.py/scienceDirect_editorEmails.csv", index = False)