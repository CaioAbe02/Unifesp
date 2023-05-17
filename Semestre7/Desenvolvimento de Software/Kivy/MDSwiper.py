from kivymd.app import MDApp
from kivy.lang import Builder

kv = '''
<MinhaSwiper@MDSwiperItem>
    # FitImage:
    #     source: "imgs/flores6.jpg"

MDScreen:
    MDTopAppBar:
        id: topappbar
        title: "Gênero de Livros"
        pos_hint: {"top": 1}

    MDSwiper:
        id: swiper
        size_hint_y: None
        height: root.height - topappbar.height - dp(40)
        y: root.height - self.height - topappbar.height - dp(20)
        on_swipe_left: app.on_swipe_left()
        on_swipe_right: app.on_swipe_right()

        MinhaSwiper:
            FitImage:
                source: "imgs/flores1.jpg"
                radius: [20]
        MinhaSwiper:
            FitImage:
                source: "imgs/flores2.jpg"
        MinhaSwiper:
            FitImage:
                source: "imgs/flores3.jpg"
        MinhaSwiper:
            FitImage:
                source: "imgs/flores4.jpg"
        MinhaSwiper:
            FitImage:
                source: "imgs/flores5.jpg"
    MDBoxLayout:
        MDRaisedButton:
            text: "Previous"
            on_release: app.action_swipe_left()
        MDRaisedButton:
            text: "Next"
            on_release: app.action_swipe_right()
'''

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        root = Builder.load_string(kv)
        return root

    def on_swipe_left(self):
        self.root.ids.topappbar.title = "Você deslizou para a esquerda"

    def on_swipe_right(self):
        self.root.ids.topappbar.title = "Você deslizou para a direita"

    def action_swipe_left(self):
        if self.root.ids.swiper.get_current_index() > 0:
            self.root.ids.swiper.set_current(self.root.ids.swiper.get_current_index() - 1)
            self.on_swipe_left()

    def action_swipe_right(self):
        if self.root.ids.swiper.get_current_index() < len(self.root.ids.swiper.get_items()) - 1:
            self.root.ids.swiper.set_current(self.root.ids.swiper.get_current_index() + 1)
            self.on_swipe_right()

MyApp().run()