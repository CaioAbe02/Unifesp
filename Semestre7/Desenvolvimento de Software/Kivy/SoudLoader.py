from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader

kv = '''
MDScreen:
    MDRaisedButton:
        id: botao
        text: "SOM"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.play_sound()

'''

class MyApp(MDApp):
    def build(self):
        self.play_music()
        return Builder.load_string(kv)

    def play_music(self):
        music = SoundLoader.load("sounds/mixkit-small-waves-harbor-rocks-1208.wav")
        music.volume = 1
        music.loop = True
        music.play()

    def play_sound(self):
        sound = SoundLoader.load("sounds/mixkit-retro-game-notification-212.wav")
        sound.volume = 0.5
        sound.play()

MyApp().run()
