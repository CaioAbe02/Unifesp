from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.clock import Clock
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from bs4 import BeautifulSoup
import requests
import json

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
STORES = ["amazon"]

class LogoScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_main_menu, 2)

    def switch_to_main_menu(self, dt):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main_menu'

class MainMenu(Screen):
    app = None
    update_prices = True
    def on_pre_enter(self, *args):
        self.app = App.get_running_app()
        self.ids.products_list.clear_widgets()
        if self.update_prices == True:
            self.get_new_prices()
            self.update_prices = False
        self.populate_list(self.ids.products_list)

    def get_new_prices(self):
        change = False
        with open("products.json", "r") as products_file:
            data = json.load(products_file)

        products = data['products']

        for product in products:
            url = product['url']
            prices = product['new_prices']
            new_price = float(self.app.get_product_price(url))

            if new_price != prices[-1]:
                prices.append(float(new_price))
                change = True

        if change:
            with open("products.json", "w") as products_file:
                json.dump(data, products_file)

    def populate_list(self, md_list):
        with open('products.json', 'r') as products_file:
            data = json.load(products_file)

        products = data['products']

        for product in products:
            name = product['name']
            original_price = product['original_price']
            new_price = product['new_prices'][-1]

            item = TwoLineIconListItem(
                text = f"[b]{name}[/b]",
                secondary_text = self.app.new_price_text(new_price, self.app.calculate_discount(original_price, new_price)),
                secondary_theme_text_color = "Custom",
                secondary_text_color = self.app.get_text_color(new_price - original_price),
            )
            item.bind(on_release=lambda instance, name=name, new_price=new_price, original_price=original_price: self.view_product(name, new_price, original_price))


            icon = IconLeftWidget(
                icon = "percent-circle-outline",
                theme_text_color = "Custom",
                text_color = self.app.get_text_color(new_price - original_price),
                icon_size = "36sp"
            )
            item.add_widget(icon)
            md_list.add_widget(item)

    def view_product(self, name, new_price, original_price):
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = 'right'
        self.manager.current = 'view_product'

        view_product_screen = self.manager.get_screen('view_product')
        view_product_screen.update_product_info(name, new_price, original_price)

class AddProduct(Screen):
    pass

class ViewProduct(Screen):
    def update_product_info(self, name, new_price, original_price):
        app = App.get_running_app()
        self.ids.product_name.text = name
        self.ids.original_price.text = f"R${original_price}"
        self.ids.discount.text = f"{app.get_number_sign(new_price - original_price)}{(app.calculate_discount(original_price, new_price))}%"
        self.ids.discount.text_color = app.get_text_color(new_price - original_price)
        self.ids.new_price.text = f"R${str(new_price)}"
        self.ids.new_price.text_color = app.get_text_color(new_price - original_price)

class WindowManager(ScreenManager):
    pass

class PrecoBom(MDApp):
    def build(self):
        main_kv = Builder.load_file("kv/main.kv")
        self.theme_cls.theme_style = "Dark"

        return main_kv

    def calculate_discount(self, original_price, new_price):
       discount = float(100 - (original_price / new_price) * 100)
       return round(discount, 1)

    def new_price_text(self, new_price, discount):
        return f"R${new_price}     {self.get_number_sign(discount)}{(discount)}%"

    def get_number_sign(self, number):
        if number > 0:
            return "+"
        return ""

    def save_product(self, product_name, product_link):
        error = self.validate_text_fields(product_name, product_link)

        if error != "":
            return error

        print("HMM")
        product_price = round(self.get_product_price(product_link), 2)


        if product_price == False:
            return "Ainda não é possível rastrear o preço desse site"


        with open("products.json", "r") as products_file:
            data = json.load(products_file)

        new_product = {
            "url": product_link,
            "name": product_name,
            "original_price": float(product_price),
            "new_prices": [float(product_price)]
        }

        data['products'].append(new_product)

        with open("products.json", "w") as product_file:
            json.dump(data, product_file)

        self.root.transition = SlideTransition()
        self.root.transition.direction = 'right'
        self.root.current = 'main_menu'

        return "Produto registrado com sucesso!"

    def validate_text_fields(self, product_name, product_link):
        if len(product_name) == 0:
            return "Nome do produto está vazio"
        elif len(product_link) == 0:
            return "Link do produto está vazio"

        if self.get_store(product_link) not in STORES:
            return "Ainda não é possível rastrear para esse site"
        try:
            page = requests.get(product_link, headers=HEADERS)

        except:
            return "Link inválido"

        return ""

    def get_product_price(self, url):
        store = self.get_store(url)
        price = None
        page = requests.get(url, headers=HEADERS)
        soup1 = BeautifulSoup(page.content, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

        print(store)
        if store == "amazon":
            price = soup2.find('span', class_='a-offscreen').text.replace("R$", "")

        print(price)

        if "." in price:
            price = price.replace(".", "")

        return price.replace(",", ".").replace(" ", "").replace("\n", "")

    def get_store(self, url):
        if "amazon" in url.strip("."):
            return "amazon"
        return None

    def get_text_color(self, number):
        if number > 0:
            return "red"
        elif number < 0:
            return "lime"
        return "yellow"

PrecoBom().run()