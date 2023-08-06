import re
from bs4 import BeautifulSoup
import requests

class WebScraper:
    def __init__(self):
        self.endpoint = "https://encore.gotlib.goteborg.se/iii/encore/search"
        self.titles = []

    def scrape_search_results(self, query):
        url = f"{self.endpoint}/{query}"
        response = requests.get(url=url)
        return BeautifulSoup(response.text, "html.parser")

    def parse_soup(self, soup):
        record_list = soup.find_all(name="div", class_="gridBrowseCol2 search-result-item__info")
        for record in record_list:
            title = record.find(name="span", class_="title").find("a").get_text().strip().replace("\r", "").replace("\n", "")
            type = record.find(name="span", class_="itemMediaDescription").get_text()
            if record.find(name="span", class_="availabilityMessage"):
                availability = record.find(name="span", class_="availabilityMessage").get_text()
            else:
                availability = ""

            self.titles.append({
                "Titel":title,
                "Typ": type,
                "Beskrivning": availability
            })
        return self.titles