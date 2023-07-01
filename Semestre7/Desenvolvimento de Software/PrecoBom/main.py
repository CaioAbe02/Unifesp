from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.clock import Clock
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget, ThreeLineIconListItem
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from bs4 import BeautifulSoup
import requests
import json
import webbrowser as wb
from kivymd_extensions.akivymd.uix.charts import AKLineChart

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
STORES = ["amazon", "kabum"]
URL_DATABASE = "https://preco-bom-ddcc1-default-rtdb.firebaseio.com/.json"

data_global = requests.get(URL_DATABASE).json()

class LogoScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_main_menu, 2)

    def switch_to_main_menu(self, dt):
        self.manager.transition = FadeTransition()
        self.manager.current = 'main_menu'

class TelaInicial(Screen):
    pass

class Padrao(Screen):
    pass

class Cadastro(Screen):
    pass

class Login(Screen):
    pass

class MainMenu(Screen):
    app = None
    update_prices = True
    data = None
    products = None
    def on_pre_enter(self, *args):
        self.app = App.get_running_app()
        self.ids.products_list.clear_widgets()
        if self.update_prices == True:
            self.data = requests.get(URL_DATABASE).json()
            self.products = self.data['products']
            # self.get_new_prices()
            self.update_prices = False
        self.populate_list(self.ids.products_list)

    def get_new_prices(self):
        change = False
        self.data = requests.get(URL_DATABASE).json()
        global data_global
        data_global = self.data
        self.products = self.data['products']

        for product in self.products:
            if product:
                url = product['url']
                prices = product['new_prices']
                new_price = float(self.app.get_product_price(url))

                if new_price != prices[-1]:
                    prices.append(float(new_price))
                    change = True

        if change:
            print(self.products)
            requests.patch(URL_DATABASE, data=json.dumps(self.data))

    def populate_list(self, md_list):
        global data_global
        data_global = self.data
        self.products = self.data['products']
        for product in self.products:
            if product:
                name = product['name']
                original_price = product['original_price']
                prices = product['new_prices']
                prices_dates = product['new_prices_dates']
                new_price = product['new_prices'][-1]
                tags = product['tags']
                url = product['url']

                item = ThreeLineIconListItem(
                    text = f"[b]{name}[/b]",
                    secondary_text = self.app.new_price_text(new_price, self.app.calculate_discount(original_price, new_price)),
                    secondary_theme_text_color = "Custom",
                    secondary_text_color = self.app.get_text_color(new_price - original_price),
                    tertiary_text = tags
                )
                item.bind(on_release=lambda instance,
                          name=name,
                          prices=prices,
                          prices_dates=prices_dates,
                          new_price=new_price,
                          original_price=original_price,
                          url=url:
                          self.view_product(name, prices, prices_dates, new_price, original_price, url))


                icon = IconLeftWidget(
                    icon = "percent-circle-outline",
                    theme_text_color = "Custom",
                    text_color = self.app.get_text_color(new_price - original_price),
                    icon_size = "36sp"
                )
                item.add_widget(icon)
                md_list.add_widget(item)

    def view_product(self, name, prices, prices_dates, new_price, original_price, url):
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = 'right'
        self.manager.current = 'view_product'

        view_product_screen = self.manager.get_screen('view_product')
        view_product_screen.update_product_info(name, prices, prices_dates, new_price, original_price, url)

class AddProduct(Screen):
    pass

class ViewProduct(Screen):
    def update_product_info(self, name, prices, prices_dates, new_price, original_price, url):
        app = App.get_running_app()
        self.ids.product_name.text = name
        self.ids.original_price.text = f"R${original_price}"
        self.ids.discount.text = f"{app.get_number_sign(new_price - original_price)}{(app.calculate_discount(original_price, new_price))}%"
        self.ids.discount.text_color = app.get_text_color(new_price - original_price)
        self.ids.new_price.text = f"R${str(new_price)}"
        self.ids.new_price.text_color = app.get_text_color(new_price - original_price)
        self.url = url

        if len(prices) > 1:
            self.build_graph(prices, prices_dates)
        else:
            self.ids.graph.clear_widgets()

    def build_graph(self, prices, prices_dates):
        linechart = AKLineChart(
            x_values = list(range(len(prices))),
            x_labels = prices_dates,
            y_values = prices,
            size_hint_y = None,
            label_size = dp(12),
            size = (dp(400), dp(300)),
            pos = [dp(0), dp(-300)],
            #circles_color
            #line_color
            #bg_color
        )

        self.ids.graph.add_widget(linechart)

    def update_product_name(self, name):
        self.ids.product_name.text = name

class Graph(Screen):
    pass

class EditProduct(Screen):
    def on_enter(self, *args):
        self.get_product_url()

    def get_product_url(self):
        view_product_screen = self.manager.get_screen('view_product')
        self.url = view_product_screen.url

    def fill_textfields(self, product_name, product_url):
        self.ids.texfield_edit_product_name.text = product_name

class Tabs(MDFloatLayout, MDTabsBase):
    pass

class GlobalProducts(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class PrecoBom(MDApp):
    def build(self):
        Builder.load_file("kv/global_products.kv")
        main_kv = Builder.load_file("kv/main.kv")
        self.theme_cls.theme_style = "Dark"

        return main_kv

    def calculate_discount(self, original_price, new_price):
       discount = float(100 - (original_price / new_price) * 100)
       return round(discount, 1)

    def new_price_text(self, new_price, discount):
        return f"R${round(float(new_price), 2)}     {self.get_number_sign(discount)}{(discount)}%"

    def get_number_sign(self, number):
        if number > 0:
            return "+"
        return ""

    def save_product(self, product_name, product_link):
        global data_global
        error = self.validate_text_fields(product_name, product_link)

        if error != "":
            return error

        product_price = round(float(self.get_product_price(product_link)), 2)


        if product_price == False:
            return "Ainda não é possível rastrear o preço desse site"

        new_product = {
            "url": product_link,
            "name": product_name,
            "original_price": float(product_price),
            "new_prices": [float(product_price)]
        }

        data_global['products'].append(new_product)
        requests.patch(URL_DATABASE, data=json.dumps(data_global))

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
        price = None
        store = self.get_store(url)
        price = None
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        page = requests.get(url, headers=headers)
        soup1 = BeautifulSoup(page.content, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

        print(store)
        if store == "amazon":
            price = soup2.find('span', class_='a-offscreen').text.replace("R$", "")
        elif store == "kabum":
            price = soup2.find('h4', class_='finalPrice').text.replace("R$", "")

        print(price)

        if "." in price:
            price = price.replace(".", "")

        return price.replace(",", ".").strip()

    def get_store(self, url):
        if "amazon" in url.strip("."):
            return "amazon"
        elif "kabum" in url.strip("."):
            return "kabum"
        return None

    def get_text_color(self, number):
        if number > 0:
            return "red"
        elif number < 0:
            return "lime"
        return "yellow"

    def visit_site(self, product_name):
        global data_global
        products = data_global['products']

        for product in products:
            if product:
                if product['name'] == product_name:
                    print(product_name)
                    wb.open(product['url'])

    def fill_edit_screen_textfields(self, product_name):
        global data_global
        products = data_global['products']

        edit_product_screen = self.root.get_screen('edit_product')

        for product in products:
            if product:
                if product['name'] == product_name:
                    edit_product_screen.fill_textfields(product_name, product['url'])

    def edit_product(self, product_name):
        global data_global

        edit_product_screen = self.root.get_screen('edit_product')
        url = edit_product_screen.url

        for product in data_global['products']:
            if product:
                if product['url'] == url:
                    product['name'] = product_name
                    break

        requests.patch(URL_DATABASE, data=json.dumps(data_global))

        view_product_screen = self.root.get_screen('view_product')
        view_product_screen.update_product_name(product_name)

        self.root.transition = SlideTransition()
        self.root.transition.direction = 'left'
        self.root.current = 'view_product'

        return ""

    def close_app(self):
        MDApp.get_running_app().stop()
        Window.close()

PrecoBom().run()