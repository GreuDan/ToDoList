from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import kivy.utils

class Informative(Popup):
    def __init__(self, **kwargs):
        super(Informative, self).__init__()
        data = kwargs['information']
        base_layout = FloatLayout()
        layout = GridLayout(cols=2, padding=100, pos_hint={"top": 1.1, "left": 1})
        popupLabel = Label(text="NAME:")
        layout.add_widget(popupLabel)
        popupLabel = Label(text="VALUE:")
        layout.add_widget(popupLabel)
        for i in data:
            if data[i] == 0:
                data[i] = "--:--"
            popupLabel = Label(text=i, color=kivy.utils.get_color_from_hex("#ffff00"))
            layout.add_widget(popupLabel)
            popupLabel = Label(text=data[i], color=kivy.utils.get_color_from_hex("#ffff00"))
            layout.add_widget(popupLabel)
        base_layout.add_widget(layout)
        closeButton = Button(text="CLOSE", color=kivy.utils.get_color_from_hex("#ffff00"),
                             background_color=kivy.utils.get_color_from_hex("#0000ff"),
                             pos_hint={"center_x": 0.5, "center_y": 0.08},
                             size_hint=(0.9, 0.1))
        base_layout.add_widget(closeButton)
        popup = Popup(title='INFORMATIVE', title_color=kivy.utils.get_color_from_hex("#ffff00"),
                      content=base_layout)
        closeButton.bind(on_press=popup.dismiss)
        popup.open()
