# Google Maps Business Scraper

A free and easy-to-use tool to scrape business information from Google Maps based on any search query. Fetch details like business name, address, phone number, website, and more.

## How to Run

First install dependencies:
```bash
pip install -r requirements.txt
```

Then run the scraper from the command line with:

```bash
python main.py -q "coffee shops New York" -max 20 -o results.xlsx --headless
```

## Arguments

**`-q` (required)**  
The Google Maps search query string.  
Example: `"pizza London"`

**`-max` (optional, default=10)**  
Maximum number of results to scrape.

**`-o` (optional, default="output.xlsx")**  
Output filename in Excel `.xlsx` format.

**`--headless` (optional)**  
Run the browser in headless mode (without UI).
