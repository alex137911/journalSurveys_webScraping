# Script to scrape names of editors-in-chief

# Remove objects in workspace
rm(list = ls())

# Required packages
suppressMessages(library(rvest))
suppressMessages(library(dplyr))
suppressMessages(library(stringi))
suppressMessages(library(data.table))
suppressMessages(library(stringr))
suppressMessages(library(tidyr))

# suppressMessages(library(rentrez))

# -------------------------------------------------------------------
# Specify the URL of the website to scrape
url <- "https://www.sciencedirect.com/browse/journals-and-books?page=1&contentType=JL&subject=medicine-and-dentistry"

# Retrieve the HTML content of website
html <- read_html(url)

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

# -------------------------------------------------------------------
# Editor URLs
journalName_df$chiefEditor <- NA

for(i in 1:nrow(journalName_df)){
  message(sprintf("%i of %i", i, nrow(journalName_df)))
  editorURL <- journalName_df$journalURL[i]
  
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
    
    # Check if "editorName" is empty (e.g., if journal is no longer in print)
    if(length(editorName) > 0) {
      journalName_df$chiefEditor[i] <- list(editorName)
    } 
    else {
      journalName_df$chiefEditor[i] <- NA
    }
  }, error = function(e){
    
    # Handle any errors that occur during scraping
    journalName_df$chiefEditor[i] <- "Error: Unable to scrape"
    print(paste("Error scraping", editorURL, ":", conditionMessage(e)))
    
  }) # end of error function
}

# Unlist the chiefEditor column
journalName_df <- unnest(journalName_df, chiefEditor)

# Store as data table (necessary for following operation)
journalName_df <- as.data.table(journalName_df)

# Remove accents from editor names
journalName_df <- journalName_df[, chiefEditor := stri_trans_general(str = chiefEditor, id = "Latin-ASCII")]

# Output directory
outpath <- "C:/Users/acale/OneDrive/Documents/Waterloo BME/Co-op/OHRI Research Internship/journalSurveys_webScraping/Data"
outDir <- sprintf("%s/Data/webScraping.R", dirname(outpath))
if(!file.exists(outDir)) dir.create(outDir)

# Drop NA rows
journalName_df <- journalName_df %>% drop_na(chiefEditor)

# Remove text after the first comma
journalName_df$modifiedName <- NA
journalName_df$modifiedName <- sub(",.*", "", journalName_df$chiefEditor)

# Drop titles (Dr., Professor, Prof., etc.)
title_pattern <- "(?i)\\b(?:Dr\\.|Professor|Prof\\.)\\s"
journalName_df$modifiedName <- gsub(title_pattern, "", journalName_df$modifiedName)

write.table(journalName_df, file = sprintf("%s/scienceDirect_chiefEditor.tsv", outDir),
            sep = "\t", row.names = FALSE, col.names = TRUE, quote = FALSE)