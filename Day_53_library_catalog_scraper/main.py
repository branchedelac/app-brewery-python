import json

from web_scraper import WebScraper
from form_filler import FormFiller
testing = False

web_scraper = WebScraper()
form_filler = FormFiller()
query = "C__Spython__Ff%3Afacetcloud%3Aprogrammering%3Aprogrammering%3Aprogrammering%3A%3A__Ff%3Afacetlanguages%3Aeng%3Aeng%3AEngelska%3A%3A__Orightresult__U__X0?lang=swe&suite=pearl"

if testing:
    # Avoid web scraping unless necessary
    with open("test_data.json") as f:
        print("using test data")
        titles = json.load(f)["titles"]
else:
    titles = web_scraper.parse_soup(web_scraper.scrape_search_results(query))

for title in titles:
    form_filler.add_via_form(title)

form_filler.close_browser()