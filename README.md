"# BMS-Events-Detail-scraping" 
"# BMS-Web-Scraping-" 
"# BMS-Web-Scraping-" 
BMS Web Scraping

Overview:
This project is a Python-based web scraping tool that extracts event details from BookMyShow for a user-specified city. It retrieves information such as event names, venues, categories, prices, and image URLs, then saves the data to an Excel file (bookmyshow_<city>events.xlsx). The HTML of the scraped page is also saved for debugging. The tool uses undetected_chromedriver, Selenium, and BeautifulSoup to handle dynamic content and potential anti-bot measures like CAPTCHAs.

Features:
Scrapes event details including name, city, venue, category, price, image URL, and promoted status.
Saves scraped data to an Excel file for easy analysis.
Saves the webpage HTML for debugging.
Handles dynamic content and scrolling to load all events.
Includes error handling for CAPTCHAs and timeouts.

Prerequisites:
Python 3.8 or higher
Google Chrome browser (compatible with undetected_chromedriver)

Installation:
1.Clone the repository:
git clone https://github.com/RoshanALokhande/BMS-Web-Scraping-.git
cd BMS-Web-Scraping-

2.Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Install ChromeDriver:
The project uses undetected_chromedriver, which automatically manages ChromeDriver. Ensure Google Chrome is installed.

Dependencies
Install the required Python packages listed in requirements.txt:

undetected-chromedriver
selenium
beautifulsoup4
pandas
openpyxl

Run:
pip install -r requirements.txt
