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
from kivymd_extensions.akivymd.uix.charts import AKLineChart
from bs4 import BeautifulSoup
import requests
import json
import webbrowser as wb
from datetime import date

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
STORES = ["amazon", "kabum", "mercadolivre"]
URL_DATABASE = "https://preco-bom-ddcc1-default-rtdb.firebaseio.com/.json"
MY_PRODUCTS_JSON = "my_products.json"

data_global = requests.get(URL_DATABASE).json()
my_data_global = json.load(open(MY_PRODUCTS_JSON))

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
    my_products = None
    def on_pre_enter(self, *args):
        self.app = App.get_running_app()
        self.ids.products_list.clear_widgets()
        self.ids.global_products.ids.global_products_list.clear_widgets()
        if self.update_prices == True:
            self.data = requests.get(URL_DATABASE).json()
            self.products = self.data['products']
            # self.get_new_prices()
            self.update_prices = False
        self.populate_my_list(self.ids.products_list)
        self.populate_global_list(self.ids.global_products.ids.global_products_list)

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

    def populate_my_list(self, md_list):
        global my_data_global

        self.my_products = my_data_global['urls']

        for my_product_url in self.my_products:
            for product in self.products:
                if product and product['url'] == my_product_url:
                    name = product['name']
                    original_price = product['original_price']
                    prices = product['new_prices']
                    prices_dates = product['new_prices_dates']
                    new_price = product['new_prices'][-1]
                    tags = product['tags']
                    url = product['url']

                    item = TwoLineIconListItem(
                        text = f"[b]{name}[/b]",
                        secondary_text = self.app.new_price_text(new_price, self.app.calculate_discount(original_price, new_price)),
                        secondary_theme_text_color = "Custom",
                        secondary_text_color = self.app.get_text_color(new_price - original_price)
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
                    break

    def view_product(self, name, prices, prices_dates, new_price, original_price, url):
        self.manager.transition = SlideTransition()
        self.manager.transition.direction = 'right'
        self.manager.current = 'view_product'

        view_product_screen = self.manager.get_screen('view_product')
        view_product_screen.update_product_info(name, prices, prices_dates, new_price, original_price, url)

    def populate_global_list(self, md_list):
        global data_global
        data_global = self.data
        self.products = self.products = sorted(self.data['products'], key=lambda x: x['name'])

        for product in self.products:
            if product:
                self.app.add_product_to_global_list(md_list, product)

class AddProduct(Screen):
    def on_leave(self, *args):
        self.clear_texts()

    def clear_texts(self):
        self.ids.texfield_product_name.text = ""
        self.ids.textfield_product_link.text = ""
        self.ids.textfield_product_tags.text = ""
        self.ids.error_text.text = ""

class ViewProduct(Screen):
    def update_product_info(self, name, prices, prices_dates, new_price, original_price, url):
        app = App.get_running_app()
        self.ids.product_name.text = name
        self.ids.original_price.text = f"R${original_price}"
        self.ids.discount.text = f"{app.get_number_sign(new_price - original_price)}{(app.calculate_discount(original_price, new_price))}%"
        self.ids.discount.text_color = app.get_text_color(new_price - original_price)
        self.ids.new_price.text = f"R${str(new_price)}"
        self.ids.new_price.text_color = app.get_text_color(new_price - original_price)
        self.ids.add_product_button.text = self.define_add_product_button(url)
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

    def define_add_product_button(self, url):
        global my_data_global

        if url in my_data_global['urls']:
            return "Remover produto"

        return "Adicionar produto"
class Graph(Screen):
    pass

class EditProduct(Screen):
    def on_enter(self, *args):
        self.get_product_url()

    def get_product_url(self):
        view_product_screen = self.manager.get_screen('view_product')
        self.url = view_product_screen.url

    def fill_textfields(self, product_name, product_tags):
        self.ids.texfield_edit_product_name.text = product_name
        self.ids.texfield_edit_product_tags.text = product_tags

class Tabs(MDFloatLayout, MDTabsBase):
    pass

class GlobalProducts(Screen):
    def on_leave(self, *args):
        self.ids.textfield_search.text = ""

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

    def save_product(self, product_name, product_link, product_tags):
        global data_global
        global my_data_global

        error = self.validate_text_fields(product_name, product_link)

        if error != "":
            return error

        product_price = self.get_product_price(product_link)

        if product_price == False:
            return "Ainda não é possível rastrear o preço desse site"
        else:
            product_price = round(float(product_price), 2)

        new_product = {
            "url": product_link,
            "name": product_name,
            "original_price": float(product_price),
            "new_prices": [float(product_price)],
            "new_prices_dates": [self.get_today_date()],
            "tags": product_tags
        }

        data_global['products'].append(new_product)
        requests.patch(URL_DATABASE, data=json.dumps(data_global))

        my_data_global['urls'].append(product_link)
        with open(MY_PRODUCTS_JSON, 'w') as file:
            json.dump(my_data_global, file)

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
            price_element = soup2.find('span', class_='a-offscreen')
            for n in range(3):
                if price_element is not None:
                    break
                else:
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

        print(price)

        if "." in price:
            price = price.replace(".", "")

        return price.replace(",", ".").strip()

    def get_store(self, url):
        if "amazon" in url.strip("."):
            return "amazon"
        elif "kabum" in url.strip("."):
            return "kabum"
        elif "mercadolivre" in url.strip("."):
            return "mercadolivre"
        return None

    def get_text_color(self, number):
        if number > 0:
            return "red"
        elif number < 0:
            return "lime"
        return "yellow"

    def get_today_date(self):
        today = date.today()
        day = str(today.day).zfill(2)
        month = str(today.month).zfill(2)
        year = str(today.year)[-2:]

        return(f"{day}/{month}/{year}")

    def visit_site(self, product_name):
        wb.open(self.root.get_screen('view_product').url)

    def fill_edit_screen_textfields(self):
        global data_global
        products = data_global['products']

        edit_product_screen = self.root.get_screen('edit_product')
        url = self.root.get_screen('view_product').url

        for product in products:
            if product:
                if product['url'] == url:
                    edit_product_screen.fill_textfields(product['name'], product['tags'])

    def edit_product(self, product_name, product_tags):
        global data_global

        edit_product_screen = self.root.get_screen('edit_product')
        url = edit_product_screen.url

        for product in data_global['products']:
            if product:
                if product['url'] == url:
                    product['name'] = product_name
                    product['tags'] = product_tags
                    break

        requests.patch(URL_DATABASE, data=json.dumps(data_global))

        view_product_screen = self.root.get_screen('view_product')
        view_product_screen.update_product_name(product_name)

        self.root.transition = SlideTransition()
        self.root.transition.direction = 'left'
        self.root.current = 'view_product'

        return ""

    def add_or_remove_product(self):
        global my_data_global
        view_product_screen = self.root.get_screen('view_product')
        url = view_product_screen.url

        if url in my_data_global['urls']:
            my_data_global['urls'].remove(url)
            view_product_screen.ids.add_product_button.text = "Adicionar produto"
        else:
            my_data_global['urls'].append(url)
            view_product_screen.ids.add_product_button.text = "Remover produto"

        with open(MY_PRODUCTS_JSON, 'w') as file:
            json.dump(my_data_global, file)

    def search_product(self, text_search):
        global data_global

        main_menu_screen = self.root.get_screen('main_menu')
        main_menu_screen.ids.global_products.ids.global_products_list.clear_widgets()

        for product in data_global['products']:
            if product:
                if text_search in product['name'] or text_search in product['tags']:
                    self.add_product_to_global_list(main_menu_screen.ids.global_products.ids.global_products_list, product)

    def add_product_to_global_list(self, md_list, product):
        name = product['name']
        original_price = product['original_price']
        prices = product['new_prices']
        prices_dates = product['new_prices_dates']
        new_price = product['new_prices'][-1]
        tags = product['tags']
        url = product['url']

        item = ThreeLineIconListItem(
            text = f"[b]{name}[/b]",
            secondary_text = self.new_price_text(new_price, self.calculate_discount(original_price, new_price)),
            secondary_theme_text_color = "Custom",
            secondary_text_color = self.get_text_color(new_price - original_price),
            tertiary_text = tags
        )
        item.bind(on_release=lambda instance,
                    name=name,
                    prices=prices,
                    prices_dates=prices_dates,
                    new_price=new_price,
                    original_price=original_price,
                    url=url:
                    self.root.get_screen('main_menu').view_product(name, prices, prices_dates, new_price, original_price, url))


        icon = IconLeftWidget(
            icon = "percent-circle-outline",
            theme_text_color = "Custom",
            text_color = self.get_text_color(new_price - original_price),
            icon_size = "36sp"
        )
        item.add_widget(icon)
        md_list.add_widget(item)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.root.get_screen('main_menu').ids.global_products.ids.textfield_search.text = ""

PrecoBom().run()