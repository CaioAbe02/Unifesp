from bs4 import BeautifulSoup
import requests
import cloudscraper
import random
import time

url = "https://www.amazon.com.br/Galax-RTX2060-12GB-1CLICK-26NRL7HP68NC/dp/B09T2GYN3F/ref=sr_1_2?__mk_pt_BR=\u00c3\u2026M\u00c3\u2026\u00c5\u00bd\u00c3\u2022\u00c3\u2018&crid=EV2EPEIFMKPA&keywords=rtx+2060&qid=1684873215&sprefix=rtx+2060%2Caps%2C323&sr=8-2&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147"

scrapers = []
for _ in range(30):
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    scrapers.append(scraper)

page = scraper.get(url)

soup      = BeautifulSoup(page.text,'html5lib')
sku_title = soup.find(id='productTitle').get_text().strip()

soup      = BeautifulSoup(page.text,'html5lib')
sku_title = soup.find(id='productTitle').get_text().strip()