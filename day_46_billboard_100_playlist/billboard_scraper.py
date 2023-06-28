import requests
from bs4 import BeautifulSoup
import requests

class BillboardScraper:
    def __init__(self):
        pass

    def scrape_billboard_hot_100(self, date):
        endpoint = "https://www.billboard.com/charts/hot-100"
        response = requests.get(url=f"{endpoint}/{date}")
        return BeautifulSoup(response.text, "html.parser")

    def parse_soup(self, soup):
        songs = []
        chart_items = soup.find_all(name="ul", class_="o-chart-results-list-row")
        for item in chart_items:
            song = {
                "title": item.find(name="h3", class_="c-title").getText().replace("\n", "").replace("\t", ""),
                "place": item.get("data-detail-target"),
                "artist": item.find(name="span", class_="c-label  a-no-trucate a-font-primary-s").getText().replace("\n", "").replace("\t",
                                                                                                              "")
            }
            songs.append(song)
        return songs