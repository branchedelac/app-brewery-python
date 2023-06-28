import re
from bs4 import BeautifulSoup
import requests

class BillboardScraper:
    def __init__(self):
        self.songs = []

    def scrape_billboard_hot_100(self, date):
        endpoint = "https://www.billboard.com/charts/hot-100"
        response = requests.get(url=f"{endpoint}/{date}")
        return BeautifulSoup(response.text, "html.parser")

    def parse_soup(self, soup):
        chart_items = soup.find_all(name="ul", class_="o-chart-results-list-row")
        for item in chart_items:
            title = item.find(name="h3", class_="c-title").getText()
            artist = item.find_all(
                name="span",
                attrs={
                    "class": re.compile('^c-label a-no-trucate a-font-primary-s.*')
                }
            )[0].getText()

            song = {
                "title": title.replace("\n", "").replace("\t", ""),
                "artist": artist.replace("\n", "").replace("\t", "")
            }
            self.songs.append(song)
        return self.songs
