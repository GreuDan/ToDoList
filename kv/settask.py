from kivy.uix.gridlayout import GridLayout
from  kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Color
import kivy.utils

class SetTask(GridLayout):
    rows=1

    def __init__(self,**kwargs):
        super(SetTask, self).__init__()
        if kwargs['data_2'] != "Done" and kwargs['data_2']!="Miss":
            color = "#e5e5e5"
            self.TaskNo_Response(color, kwargs['data_1'], kwargs['data_2'])

        else:
            if kwargs['data_2'] == "Miss":
                color = "ff0000"
                self.TaskResponded_Miss(color,kwargs['data_1'])
            else:
                color = "00ff00"
                self.TaskResponded_Done(color, kwargs['data_1'])


    def DisableButtons(self,status):
        self.remove_widget(self.left2)
        if status==1:
            self.left_label2.text="Done"
            with self.canvas.before:
                self.UpColor = Color(rgb=kivy.utils.get_color_from_hex("#00ff00"))
                self.rectangle = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.update_rectangle, size=self.update_rectangle)
        else:
            self.left_label2.text = "Removed"
            with self.canvas.before:
                self.UpColor = Color(rgb=kivy.utils.get_color_from_hex("#ff0000"))
                self.rectangle = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.update_rectangle, size=self.update_rectangle)
    def response(self):
        try:
            return self.Done,self.Delete
        except:
            return 0,0

    def update_rectangle(self,*args):
        self.rectangle.pos=self.pos
        self.rectangle.size = self.size
    def TaskResponded_Done(self,color,name):
        with self.canvas.before:
            Color(rgb=kivy.utils.get_color_from_hex(color))
            self.rectangle = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rectangle, size=self.update_rectangle)
        left = FloatLayout()
        left_label1 = Label(text=name, color=kivy.utils.get_color_from_hex("#000000"),
                            size_hint=(.1, .8), pos_hint=({"top": .9, "right": .6}))
        left.add_widget(left_label1)
        left1 = FloatLayout()
        left_label2 = Label(text="Done", color=kivy.utils.get_color_from_hex("#000000"),
                            size_hint=(.1, .8), pos_hint=({"top": .9, "right": .6}))
        left1.add_widget(left_label2)

        self.add_widget(left)
        self.add_widget(left1)
    def TaskResponded_Miss(self,color,name):
        with self.canvas.before:
            Color(rgb=kivy.utils.get_color_from_hex(color))
            self.rectangle = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rectangle, size=self.update_rectangle)
        left = FloatLayout()
        left_label1 = Label(text=name, color=kivy.utils.get_color_from_hex("#000000"),
                            size_hint=(.1, .8), pos_hint=({"top": .9, "right": .6}))
        left.add_widget(left_label1)
        left1 = FloatLayout()
        left_label2 = Label(text="Miss", color=kivy.utils.get_color_from_hex("#000000"),
                            size_hint=(.1, .8), pos_hint=({"top": .9, "right": .6}))
        left1.add_widget(left_label2)

        self.add_widget(left)
        self.add_widget(left1)
    def TaskNo_Response(self,color,name,time):
        with self.canvas.before:
            self.UpColor=Color(rgb=kivy.utils.get_color_from_hex(color))
            self.rectangle = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rectangle, size=self.update_rectangle)
        self.left = FloatLayout()
        self.left_label1 = Label(text=name, color=kivy.utils.get_color_from_hex("#000000"),
                            size_hint=(.1, .8), pos_hint=({"top": .9, "right": .6}))
        self.left.add_widget(self.left_label1)
        self.left1 = FloatLayout()
        self.left_label2 = Label(text=time, color=kivy.utils.get_color_from_hex("#000000"),
                            size_hint=(.1, .8), pos_hint=({"top": .9, "right": .6}))
        self.left1.add_widget(self.left_label2)

        self.left2 = FloatLayout()
        self.Done = Button(text="Done", size_hint=(.3, .8), pos_hint=({"top": .9, "right": .5}))
        self.left2.add_widget(self.Done)
        self.Delete = Button(text="Delete", size_hint=(.3, .8), pos_hint=({"top": .9, "right": .9}))
        self.left2.add_widget(self.Delete)

        self.add_widget(self.left)
        self.add_widget(self.left1)
        self.add_widget(self.left2)




