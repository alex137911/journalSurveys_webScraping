# Script to scrape names of Editors-in-Chief

# Remove objects in workspace
rm(list = ls())

# Required packages
suppressMessages(library(rvest))
suppressMessages(library(dplyr))
suppressMessages(library(stringi))
suppressMessages(library(data.table))
suppressMessages(library(stringr))
suppressMessages(library(tidyr))

# -------------------------------------------------------------------
# Specify the base URL pattern
base_url <- "https://www.sciencedirect.com/browse/journals-and-books?page=%d&contentType=JL&subject=medicine-and-dentistry"
base_url <- "https://www.sciencedirect.com/browse/journals-and-books?contentType=JL&subject=nursing-and-health-professions"

# Number of pages to scrape
num_pages <- 3

# Initialize an empty data table to store the final results
all_journalData <- data.table()

# Loop through the page numbers
for(page_number in 1:num_pages){
  message(sprintf("Scraping Page %d of %d", page_number, num_pages))
  
  # Construct the URL for the current page
  url <- sprintf(base_url, page_number)
  
  # Retrieve the HTML content of the current page
  html <- read_html(url)
  
  # Process the HTML content
  # Pull journal names
  journalNode <- html_nodes(html, ".js-publication")
  journalName <- html_text(journalNode)
  
  # Store as data frame
  journalName_df <- as.data.frame(journalName)
  
  # Science direct journal URL template: www.sciencedirect.com/journal/journal-name
  # Remove characters that are not part of journal titles
  journalName_df$journalName <- gsub("\\•..*", "", journalName_df$journalName)
  
  # Remove "Journal" from titles (i.e., last 7 characters of each string)
  removeLast_n <- 7
  journalName_df$journalName <- str_trim(journalName_df$journalName, side = "right")
  journalName_df$journalName <- substr(journalName_df$journalName, 1, 
                                       nchar(journalName_df$journalName) - removeLast_n)
  # Remove parentheses from journal titles
  journalName_df$journalName <- gsub("\\(|\\)", "", journalName_df$journalName)
  
  # Replace "&" with "and" in journal titles
  journalName_df$journalName <- gsub("\\&", "and", journalName_df$journalName)
  
  # Remove " - " in journal titles  
  journalName_df$journalName <- gsub("\\ - ", " ", journalName_df$journalName)
  
  # Remove apostrophe (') in journal titles 
  journalName_df$journalName <- gsub("\\'", "", journalName_df$journalName)
  
  # Remove ":" in journal titles
  journalName_df$journalName <- gsub("\\:", "", journalName_df$journalName)
  
  # Replace spaces with "-"
  journalName_df$journalName <- gsub(" ", "-", journalName_df$journalName)
  
  # Store as data table (necessary for following operation)
  journalName_df <- as.data.table(journalName_df)
  
  # Remove accents from journal titles (e.g., English versions of foreign journals)
  # https://stackoverflow.com/a/56595128/15269111
  journalName_df <- journalName_df[, journalName := stri_trans_general(str = journalName, id = "Latin-ASCII")]
  
  # Remove white spaces
  journalName_df$journalName <- str_trim(journalName_df$journalName, side = "right")
  
  # Create URLs
  journalName_df$journalURL <- NA
  
  for(i in 1:nrow(journalName_df)){
    journalName_df$journalURL[i] <- paste0("www.sciencedirect.com/journal/", "", journalName_df$journalName[i])
  }
  
  # Append the data from this iteration to the final data table
  all_journalData <- rbind(all_journalData, journalName_df)
}

# -------------------------------------------------------------------
# Editor URLs
all_journalData$chiefEditor <- NA

for(i in 274:nrow(all_journalData)){
  message(sprintf("%i of %i", i, nrow(all_journalData)))
  editorURL <- all_journalData$journalURL[i]
  
  # Check if the URL is missing the protocol and prepend "https://"
  if(!grepl("^https?://", editorURL, ignore.case = TRUE)) {
    editorURL <- paste0("https://", editorURL)
  }
  
  tryCatch({
    # Retrieve the HTML content of website
    editorHTML <- read_html(editorURL)
    
    # Pull editor
    editorNode <- html_nodes(editorHTML, ".js-editor-name")
    editorName <- html_text(editorNode)
    
    
    # Introduce a slight delay to avoid overloading the server
    Sys.sleep(1)
   
    # Pull editor
    editorNode <- html_nodes(editorHTML, ".js-editor-name")
    editorName <- html_text(editorNode)
    
    # Check if "editorName" is empty (e.g., if journal is no longer in print)
    if(length(editorName) > 0) {
      all_journalData$chiefEditor[i] <- list(editorName)
    } 
    else {
      all_journalData$chiefEditor[i] <- NA
    }
  }, error = function(e){
    
    # Handle any errors that occur during scraping
    all_journalData$chiefEditor[i] <- "Error: Unable to scrape"
    print(paste("Error scraping", editorURL, ":", conditionMessage(e)))
    
  }) # end of error function
}

# Unlist the chiefEditor column
all_journalData <- unnest(all_journalData, chiefEditor)

# Store as data table (necessary for following operation)
all_journalData <- as.data.table(all_journalData)

# Remove accents from editor names
all_journalData <- all_journalData[, chiefEditor := stri_trans_general(str = chiefEditor, id = "Latin-ASCII")]

# Drop NA rows
all_journalData <- all_journalData %>% drop_na(chiefEditor)

# Remove text after the first comma
all_journalData$modifiedName <- NA
all_journalData$modifiedName <- sub(",.*", "", all_journalData$chiefEditor)

# Drop titles (Dr., Professor, Prof., etc.)
title_pattern <- "(?i)\\b(?:Dr\\.|Professor|Prof\\.|Assist\\.|Assoc\\.|Mr\\.|Ms\\.|Mrs\\.|PD med\\.)\\s"
all_journalData$modifiedName <- gsub(title_pattern, "", all_journalData$modifiedName)

# -------------------------------------------------------------------
# Output directory
outpath <- "C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data"
outDir <- sprintf("%s/Data/webScraping.R", dirname(outpath))
if(!file.exists(outDir)) dir.create(outDir)

write.table(all_journalData, file = sprintf("%s/scienceDirect_chiefEditor.tsv", outDir),
            sep = "\t", row.names = FALSE, col.names = TRUE, quote = FALSE)