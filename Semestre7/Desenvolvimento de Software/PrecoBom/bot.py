from bs4 import BeautifulSoup
import requests
import json
from datetime import date
import time
from colorama import Fore, Style

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
            dates = product['new_prices_dates']
            new_price = get_product_price(url)

            if not new_price:
                print(Fore.RED + f"\n\n-= Não foi possível atualizar o preço de {product['name']} =-\n\n")
            else:
                new_price = float(new_price)

                if new_price != prices[-1]:
                    prices.append(float(new_price))
                    dates.append(get_today_date())
                    change = True
                    print(Fore.GREEN + f"\n\n-= Novo preço para {product['name']}: R${new_price} =-\n\n")
                else:
                    print(Fore.YELLOW + f"\n\n-= {product['name']} não mudou de preço =-\n\n")


        time.sleep(1)

    if change:
        requests.patch(URL_DATABASE, data=json.dumps(data))

def get_product_price(url):
    price = None
    store = get_store(url)
    page = requests.get(url, headers=HEADERS)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    if store == "amazon":
        price_element = soup2.find('span', class_='a-offscreen')
    elif store == "kabum":
        price_element = soup2.find('h4', class_='finalPrice')
    elif store == "mercadolivre":
        div = soup2.find('div', class_='ui-pdp-price__second-line')
        price_element = div.find('span', class_='andes-money-amount__fraction')
        price_cents = div.find('span', class_='andes-money-amount__cents')

    if price_element is not None:
        price = price_element.text.replace("R$", "")

        if store == "mercadolivre" and price_cents is not None:
            price_cents = price_cents.text.strip()
            price = f"{price.strip()},{price_cents}"

    else:
        return False

    if "." in price:
        price = price.replace(".", "")

    # print(price)

    return price.replace(",", ".").strip()

def get_store(url):
    if "amazon" in url.strip("."):
        return "amazon"
    elif "kabum" in url.strip("."):
        return "kabum"
    elif "mercadolivre" in url.strip("."):
        return "mercadolivre"
    return None

def get_today_date():
    today = date.today()
    day = str(today.day).zfill(2)
    month = str(today.month).zfill(2)
    year = str(today.year)[-2:]

    return(f"{day}/{month}/{year}")

if __name__ == "__main__":
    get_new_prices()
    print(Style.RESET_ALL)