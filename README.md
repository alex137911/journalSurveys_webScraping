# Web  Scraping for Journal Surveys
Work for Dr. Jeremy Y. Ng

### Project Goal
Scrape emails of Editors-in-Chief for different scientific journals

### Project Status
- [x] Scrape journal URLS
- [x] Scrape names of Editors-in-Chief
- [x] Find emails of Editors-in-Chief through PubMed search
- [ ] Expand to journals outside of Science Direct 

#### Environment Setup
==Using Chrome WebDriver==
1. Download Chromedriver: Visit the official Chromedriver download page (https://sites.google.com/a/chromium.org/chromedriver/downloads) and download the appropriate version of Chromedriver that matches your Chrome browser version.

2. Extract Chromedriver: Extract the downloaded Chromedriver executable to a location on your computer.

3. Add Chromedriver to PATH: Add the path to the Chromedriver executable to your system's PATH environment variable. This allows your Python script to locate the Chromedriver executable.
    a) Windows: Open the Start menu, search for "Environment Variables," and select "Edit the system environment variables." In the System Properties window, click the "Environment Variables" button. In the "System Variables" section, select the "Path" variable, and click the "Edit" button. Add the path to the Chromedriver executable (e.g., C:\path\to\chromedriver) to the list of paths. Click "OK" to save the changes.
    b) macOS/Linux: Open a terminal and edit the .bash_profile or .bashrc file in your home directory using a text editor (e.g., nano ~/.bash_profile). Add the following line to the file: export PATH=$PATH:/path/to/chromedriver (replace /path/to/chromedriver with the actual path to the Chromedriver executable). Save the file and then run source ~/.bash_profile or source ~/.bashrc to apply the changes.

4. Verify installation: Open a new terminal or command prompt and run chromedriver command to verify if Chromedriver is now accessible from the system's PATH. If it prints version information without any errors, the installation was successful. 