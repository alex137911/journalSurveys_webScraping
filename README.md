# Web  Scraping for Journal Surveys
Work for Dr. Jeremy Y. Ng

### Project Goal
Scrape emails of Editors-in-Chief for different scientific journals

### Project Status
- [x] Scrape journal URLS
- [x] Scrape names of Editors-in-Chief
- [x] Find emails of Editors-in-Chief through PubMed search
- [ ] Expand to journals outside of Science Direct 
---
### About
The work to scrape the email addresses of the editors are broken into two scripts and must be run in the following order:
1. webScraping.R
2. editorEmails.py

Currently, *webScraping.R* only supports journals published by ScienceDirect.

#
#### Environment Setup: webScraping.R
This script is used to retrieve the HTML content of the different ScienceDirect journals and scrape the name(s) of the Editor(s)-in-Chief. Note that in order to retrieve the journal URLs as well as successfully search through PubMed, titles and names must be converted to the "standard" English alphabet. The preprocessing done in this script may not cover all cases. 

This script was developed using R version 4.2.2 (2022-10-31 ucrt) -- "Innocent and Trusting", and the following packages are used and must be intalled:
1. rvest
2. dplyr
3. stringi
4. data.table
5. stringr
6. tidyr

The final output of this script is a .tsv file including the **journal title** ("journalName"), the **journal URL** ("journalURL"), the **editor names** ("chiefEditor") and the **modified name** ("modifiedName") with titles and designations removed.

#
#### Environment Setup: editorEmails.py
Once the *webScraping.R* script has been run to produce the .tsv file, this script pulls the names of the editors to search through PubMed and find the editors' emails (through their publicly available articles). The matching algorithm to retrieve the correct email for the corresponding Editor-in-Chief works as follows:

1. The function, *calculate_match()*, takes two text inputs: the name, and the name derived from the email (i.e., all characters before the @ in the email address).
2. The function converts both the name and the name from the email to lowercase letters. This is done to make sure the comparison is not case-sensitive. For example, "John" and "john" would be considered the same.
3. The function then compares the two texts and calculates a number called the "matching rate" between them. This number represents how similar the name is to the name from the email.[^1]
4. The higher the "matching rate," the more similar the name and email are to each other. If the matching rate is 100, it means the name and email are exactly the same. If it's 0, it means they are completely different.
5. The function then returns this matching rate as the result.

[^1]: The matching rate is calculated based on the number of common tokens and their order. It gives higher importance to the order of the tokens because it takes into account the word sequence. For example, let's say the editor's name is "John Doe" and the email address is "john.doe@example.com." The tokenization process would split the name and the email into tokens like this:
Editor's Name Tokens: ["John", "Doe"]
Email Name Tokens: ["john", "doe"]
before sorting the tokens alphabetically for comparison. The function then calculates the matching rate based on the number of common tokens and their order between the two strings. Since the tokens have been sorted, it can still find a match even if the original strings have some variations or are in a different order. However, the **matching rate will be higher when the tokens appear in the same order in both strings**. These tokens are then compared to calculate a similarity score between the name and the email.

**Please note!** The code only iterates through a maximum of 10 articles (which can be changed by the user if necessary), and as such, **may not identify the correct email address with 100% accuracy** (or in some cases, will not find an email address at all). A confidence score (i.e., the matching rate) is provided in the final column of the .csv output, where a higher score (maximum 100) indicates a better match between the email address and the editor's name. If possible, it is strongly encouraged that a manual check is performed.

<ins>Using Chrome WebDriver</ins>
1. Download Chromedriver: Visit the official Chromedriver download page (https://sites.google.com/a/chromium.org/chromedriver/downloads) and download the appropriate version of Chromedriver that matches your Chrome browser version.

2. Extract Chromedriver: Extract the downloaded Chromedriver executable to a location on your computer.

3. Add Chromedriver to PATH:

   | Operating System | Steps |
   | --- | --- |
   | Windows | **1.** Open the Start menu, search for "Environment Variables," and select "Edit the system environment variables." **2.** In the System Properties window, click the "Environment Variables" button. In the "System Variables" section, select the "Path" variable, and click the "Edit" button. **3.** Add the path to the Chromedriver executable (e.g., C:\path\to\chromedriver) to the list of paths. **4.** Click "OK" to save the changes. |
   | macOS/Linux | **1.** Open a terminal and edit the .bash_profile or .bashrc file in your home directory using a text editor (e.g., nano ~/.bash_profile). **2.** Add the following line to the file: `export PATH=$PATH:/path/to/chromedriver` (replace `/path/to/chromedriver` with the actual path to the Chromedriver executable). **3.** Save the file and then run `source ~/.bash_profile` or `source ~/.bashrc` to apply the changes. |


4. Verify installation: Open a new terminal or command prompt and run chromedriver command to verify if Chromedriver is now accessible from the system's PATH. If it prints version information without any errors, the installation was successful. 
