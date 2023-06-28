from bs4 import BeautifulSoup
import requests
import json

URL_DATABASE = "https://preco-bom-ddcc1-default-rtdb.firebaseio.com/.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

def get_new_prices():
    data = requests.get(URL_DATABASE).json()
    products = data['products']
    change = False

    for product in products:
        if product:
            url = product['url']
            prices = product['new_prices']
            new_price = float(get_product_price(url))

            if new_price != prices[-1]:
                    prices.append(float(new_price))
                    change = True

    if change:
        requests.patch(URL_DATABASE, data=json.dumps(data))

def get_product_price(url):
    price = None
    store = get_store(url)
    page = requests.get(url, headers=HEADERS)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    if store == "amazon":
        price = soup2.find('span', class_='a-offscreen').text.replace("R$", "")
    elif store == "kabum":
        price = soup2.find('h4', class_='finalPrice').text.replace("R$", "")

    if "." in price:
        price = price.replace(".", "")

    print(price)

    return price.replace(",", ".").strip()

def get_store(url):
    if "amazon" in url.strip("."):
        return "amazon"
    elif "kabum" in url.strip("."):
        return "kabum"
    return None

if __name__ == "__main__":
    get_new_prices()