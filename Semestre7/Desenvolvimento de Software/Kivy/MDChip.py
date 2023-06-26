from kivy.lang import Builder
from kivymd.app import MDApp

kv = '''
MDBoxLayout:
    orientation: "vertical"
    spacing: dp(10)
    MDTopAppBar:
        title: app.title
        md_bg_color: app.theme_cls.primary_color
        left_action_items: [["menu", lambda x: x]]
        background_palette: "Primary"

    ScrollView:
        id: scrollview
        MDGridLayout:
            padding: dp(10)
            spacing: dp(10)
            cols: 1
            adaptive_height: True
            Widget:
                size_hint_y: .5
                heigh: dp(15)
            MDLabel:
                text: "Chips com cor"
            MDSeparator:
            MDStackLayout:
                adaptive_height: True
                spacing: dp(10)
                MDChip:
                    text: "Coffee"
                    md_bg_color: .45, .2, 0, 1
                    text_color: "white"
                MDChip:
                    text: "Lime"
                    md_bg_color: 36/255, 252/255, 3/255, 1
                    text_color: "white"
                MDChip:
                    text: "Apple"
                    md_bg_color: 252/255, 3/252, 28/255, 1
                    text_color: "white"
                MDChip:
                    text: "Banana"
                    md_bg_color: 252/255, 215/255, 3/255, 1
                    text_color: "white"

            Widget:
                size_hint_y: .5
                heigh: dp(10)
            MDLabel:
                text: "Chips com ícone"
            MDSeparator:
            MDStackLayout:
                adaptive_height: True
                spacing: dp(10)
                MDChip:
                    text: "Sem"
                    md_bg_color: 160/255, 160/255, 160/255, 1
                    text_color: "white"
                MDChip:
                    text: "Esquerda"
                    md_bg_color: 160/255, 160/255, 160/255, 1
                    text_color: "white"
                    icon_left: "close-circle-outline"
                MDChip:
                    text: "Direita"
                    md_bg_color: 160/255, 160/255, 160/255, 1
                    text_color: "white"
                    icon_right: "close-circle-outline"
                MDChip:
                    text: "Dois"
                    md_bg_color: 160/255, 160/255, 160/255, 1
                    text_color: "white"
                    icon_left: "close-circle-outline"
                    icon_right: "close-circle-outline"

            Widget:
                size_hint_y: .5
                heigh: dp(15)
            MDLabel:
                text: "Escolha um Chip"
            MDSeparator:
            MDChip:
                text: "Chip"
                md_bg_color: 160/255, 160/255, 160/255, 1
                text_color: "white"
                on_active: if self.active: app.remove_marks_all_chips(self)
            MDChip:
                text: "Chip"
                md_bg_color: 160/255, 160/255, 160/255, 1
                text_color: "white"
                on_active: if self.active: app.remove_marks_all_chips(self)
            MDChip:
                text: "Chip"
                md_bg_color: 160/255, 160/255, 160/255, 1
                text_color: "white"
                on_active: if self.active: app.remove_marks_all_chips(self)
'''

class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Exemplo de MDChips"
        self.theme_cls.primary_palette = "Red"

    def build(self):
        self.root = Builder.load_string(kv)

    def remove_marks_all_chips(self, selected_chip):
        g = self.root.ids.scrollview.children

        for instance_chip in g[0].children:
            if instance_chip.ids != {} and instance_chip != selected_chip:
                instance_chip.active = False

Test().run()