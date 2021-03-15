import json
import time
import os
import sys
import kivy.utils
import requests
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from datetime import datetime
from kv.firebaseconnection import FirebaseConnection
from kv.informativepopup import InformativePopup
from kv.settask import SetTask

class ImageButton(ButtonBehavior, Image):
    pass

class ScheduelScreen(Screen):
    pass

class NotificationScreen(Screen):
    pass

class IstoricScreen(Screen):
    pass

class AccountScreen(Screen):
    pass

class AuthentificationScreen(Screen):
    pass

class AddFriendScreen(Screen):
    pass

class AddTaskScreen(Screen):
    pass

class MainApp(App):
    def build(self):
        self.current = 0
        self.Done_1 = 0
        self.Done_2 = 0
        self.Done_3 = 0
        self.Undone_1 = 0
        self.Undone_2 = 0
        self.Undone_3 = 0
        self.DeleteDone = []
        self.database = FirebaseConnection()
        return Builder.load_file("main.kv")

    def ReFill(self):
        check = self.data['Repeats']
        monthly = check['Once a Month']
        for element in monthly:
            if str(datetime.now().day) == str(monthly[element]['Date']):
                task = '{"Name":"' + str(monthly[element]['Name']) + '","Time":"' + str(monthly[element]['Time']) + '"}'
                requests.post(
                    'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task.json?auth=' + self.id_token,
                    data=task)
        weekly = check['Once a Week']
        for element in weekly:
            if str(datetime.now().weekday()) == str(weekly[element]['Date']):
                task = '{"Name":"' + str(weekly[element]['Name']) + '","Time":"' + str(
                    weekly[element]['Time']) + '"}'
                requests.post(
                    'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task.json?auth=' + self.id_token,
                    data=task)
        daily=check['Daily']
        for element in daily:
            task = '{"Name":"' + str(daily[element]['Name']) + '","Time":"' + str(
                daily[element]['Time']) + '"}'
            requests.post(
                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task.json?auth=' + self.id_token,
                data=task)
        tomorrow = check['Tomorrow tasks']
        for element in tomorrow:
            if tomorrow[element]['Name']!="Default":
                task = '{"Name":"' + str(tomorrow[element]['Name']) + '","Time":"' + str(
                    tomorrow[element]['Time']) + '"}'
                requests.post(
                    'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task.json?auth=' + self.id_token,
                    data=task)

    def LastCheck(self):
        try:
            self.request = requests.get(self.adress)
            self.data = json.loads(self.request.content.decode())
            date=self.data['Day']
            if date=="":
                month=datetime.now().month
                day=datetime.now().day
                date=str(month)+":"+str(day)+":"+"1"
                setDay='{"Day":"'+date+'"}'
                requests.patch(self.adress,data=setDay)
            else:
                month, day,count = self.data['Day'].split(":")
                count=int(count)
                if str(datetime.now().month) != month and str(datetime.now().day) != day:
                    month = str(datetime.now().month)
                    day = str(datetime.now().day)
                    count+=1
                    date = str(month) + ":" + str(day)+":"+str(count)
                    setDay= '{"Day":"' + date + '"}'
                    requests.patch(self.adress, data=setDay)
                    self.ReFill()
                else:
                    if str(datetime.now().day) != day:
                        day = str(datetime.now().day)
                        count += 1
                        date = str(month) + ":" + str(day) + ":" + str(count)
                        setDay = '{"Day":"' + date + '"}'
                        requests.patch(self.adress, data=setDay)
                        zero_today = self.data['Today Task']
                        history_events = ""
                        for element in zero_today:
                            if zero_today[element]["Name"] != "Default":
                                try:
                                    history_events += zero_today[element]["Name"] + "-" + zero_today[element]["Time"] + "-"
                                    requests.delete(
                                        'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task/' + str(
                                            element) + '.json?auth=' + self.id_token)
                                except:
                                    pass
                        history_day = str(day) + "." + str(month) + "." + str(datetime.now().year)
                        new_historic = '{"Date":"%s"' % history_day + ',"Events":"%s"}' % history_events
                        a = requests.post(
                            'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/History/.json?auth=' + self.id_token,
                            data=new_historic)
                        self.IstoricFill()
                        try:
                            self.ReFill()
                        except:
                            pass

        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass
    def on_start(self):
        try:
            with open("kv/refreshToken.txt", "r") as save_file:
                refreshToken = save_file.read()
            self.id_token, self.local_id = self.database.exchange_refresh_token(refreshToken)
            self.request = requests.get(
                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '.json?auth=' + self.id_token)
            self.adress = 'https://todo-list-737ca.firebaseio.com/' + self.local_id + '.json?auth=' + self.id_token
            self.data = json.loads(self.request.content.decode())
            self.LastCheck()
            self.AccountFill()
            self.ScheduelFill()
            self.IstoricFill()
            self.root.transition = NoTransition()
            self.root.current = "scheduel_screen"
            self.root.transition = CardTransition()
        except:
            pass

    def AccountFill(self):
        try:
            self.request = requests.get(self.adress)
            self.data = json.loads(self.request.content.decode())
            self.root.ids['account_screen'].ids['label_2'].text = str(self.data["Name"])
            self.root.ids['account_screen'].ids['label_4'].text = str(self.data["ID"])
            self.root.ids['account_screen'].ids['label_6'].text = str(self.data["Email"])
            account_manager = self.data["Account"]
            a = account_manager["Today Tasks"]
            self.root.ids['account_screen'].ids['label_9'].text = str(a["Done"])
            self.Done_1 = int(a["Done"])
            self.root.ids['account_screen'].ids['label_11'].text = str(a["Undone"])
            self.Undone_1 = int(a["Undone"])
            a = account_manager["Yesterday Tasks"]
            self.root.ids['account_screen'].ids['label_14'].text = str(a["Done"])
            self.Done_2 = int(a["Done"])
            self.root.ids['account_screen'].ids['label_16'].text = str(a["Undone"])
            self.Undone_2 = int(a["Undone"])
            a = account_manager["Week Tasks"]
            self.root.ids['account_screen'].ids['label_19'].text = str(a["Done"])
            self.Done_3 = int(a["Done"])
            self.root.ids['account_screen'].ids['label_21'].text = str(a["Undone"])
            self.Undone_3 = int(a["Undone"])
        except:
            pass

    def DeleteTask(self,a,widget,name, time):
        self.request = requests.get(self.adress)
        self.data = json.loads(self.request.content.decode())
        try:
            dates = self.data['Today Task']
            for i in dates:
                if dates[i]["Name"] == str(name) and dates[i]["Time"] == str(time):
                    try:
                        a1=0
                        requests.delete(
                            'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task/' + str(
                                i) + '.json?auth=' + self.id_token)
                        widget.DisableButtons(a1)
                    except Exception as e :
                        print(e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        pass
        except:
            pass

    def DoneTask(self, a, widget, task_name, task_time):
        self.AccountFill()
        a1=1
        Done_1 = self.Done_1 + 1
        Done_3 = self.Done_3 + 1
        upd_done = '{"Account": {"Today Tasks": {"Done": "' + str(Done_1) + '", "Undone": "' + str(
            self.Undone_1) + '"}, "Week Tasks": ' \
                             '{"Done": "' + str(Done_3) + '",' \
                                                          ' "Undone": "' + str(
            self.Undone_3) + '"},"Yesterday Tasks": {"Done": "' + str(self.Done_2) + '", "Undone": "' + str(
            self.Undone_2) + '' \
                             '"}}}'
        self.adress = 'https://todo-list-737ca.firebaseio.com/' + self.local_id + '.json?auth=' + self.id_token
        requests.patch(self.adress, data=upd_done)
        try:
            self.request = requests.get(self.adress)
            self.data = json.loads(self.request.content.decode())
            try:
                dates = self.data['Today Task']
                for i in dates:
                    if dates[i]["Name"] == str(task_name) and dates[i]["Time"] == str(task_time):
                        try:
                            data = '{"Name":"' + str(task_name) + '","Time":"Done"}'
                            requests.delete(
                                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task/' + str(
                                    i) + '.json?auth=' + self.id_token)
                            requests.post(
                                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task/.json?auth=' + self.id_token,
                                data=data)
                            widget.DisableButtons(a1)
                        except:
                            pass
            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                pass
        except:
            pass

    def MissTask(self, name, time):
        self.AccountFill()
        Undone_1 = self.Undone_1 + 1
        Undone_3 = self.Undone_3 + 1
        upd_undone = '{"Account": {"Today Tasks": {"Done": "' + str(self.Done_1) + '", "Undone": "' + str(
            Undone_1) + '"}, "Week Tasks": ' \
                        '{"Done": "' + str(self.Done_3) + '",' \
                                                          ' "Undone": "' + str(
            Undone_3) + '"},"Yesterday Tasks": {"Done": "' + str(self.Done_2) + '", "Undone": "' + str(
            self.Undone_2) + '' \
                             '"}}}'
        requests.patch(self.adress, data=upd_undone)
        try:
            self.request = requests.get(self.adress)
            self.data = json.loads(self.request.content.decode())
            try:
                dates = self.data['Today Task']
                for i in dates:
                    if dates[i]["Name"] == str(name) and dates[i]["Time"] == str(time):
                        try:
                            data = '{"Name":"' + str(name) + '","Time":"Miss"}'
                            requests.delete(
                                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task/' + str(
                                    i) + '.json?auth=' + self.id_token)
                            requests.post(
                                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task/.json?auth=' + self.id_token,
                                data=data)
                            return "Miss"
                        except:
                            pass
            except:
                pass
        except:
            pass

    def ScheduelFill(self):
        try:
            self.request = requests.get(self.adress)
            self.data = json.loads(self.request.content.decode())
            origin = self.root.ids['scheduel_screen'].ids['task_banner']
            dates = self.data['Today Task']
            try:
                for element in dates:
                    if dates[element]["Name"] != "Default":
                        if dates[element]["Time"]!= "Done" and dates[element]["Time"]!= "Miss":
                            try:
                                hour, minute = dates[element]["Time"].split(":")
                                if int(datetime.now().hour) > int(hour):
                                    dates[element]["Time"] = self.MissTask(dates[element]["Name"],
                                                                           dates[element]["Time"])
                                else:
                                    if int(datetime.now().hour) == int(hour) and int(datetime.now().minute) > int(
                                            minute):
                                        dates[element]["Time"] = self.MissTask(dates[element]["Name"],
                                                                               dates[element]["Time"])
                            except Exception as e:
                                print(e)
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno)
                                pass
                            self.task = SetTask(data_1=dates[element]["Name"], data_2=dates[element]["Time"])
                            done, delete = self.task.response()
                            origin.add_widget(self.task)
                            self.DeleteDone.append(delete)
                            if self.current % 2 == 0:
                                self.DeleteDone[self.current].bind(
                                    on_release=lambda a, widget=self.task, name_task=dates[element]["Name"],
                                                      time_task=dates[element][
                                                          "Time"]: self.DeleteTask(a, self.task,
                                                                                   name_task,
                                                                                   time_task))
                                self.current += 1
                            self.DeleteDone.append(done)
                            if self.current % 2 != 0:
                                self.DeleteDone[self.current].bind(
                                    on_release=lambda a, name_task=dates[element]["Name"],
                                                      time_task=dates[element][
                                                          "Time"]: self.DoneTask(a, self.task,
                                                                                 name_task,
                                                                                 time_task))
                                self.current += 1
                        else:
                            if dates[element]["Time"]=="Done":
                                try:
                                    self.task = SetTask(data_1=dates[element]["Name"], data_2="Done")
                                    origin.add_widget(self.task)
                                except Exception as e:
                                    print(e)
                                    exc_type, exc_obj, exc_tb = sys.exc_info()
                                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                    print(exc_type, fname, exc_tb.tb_lineno)

                            else:
                                self.task = SetTask(data_1=dates[element]["Name"], data_2="Miss")
                                origin.add_widget(self.task)

            except Exception as e:
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                pass
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass

    def AddTask(self, name, hour, minute, repeats):
        origin = self.root.ids['scheduel_screen'].ids['task_banner']
        time = str(hour) + ":" + str(minute)
        self.AccountFill()

        task = '{"Name":"' + str(name) + '","Time":"' + str(time) + '"}'
        if int(datetime.now().hour) == int(hour) and int(datetime.now().minute) > int(minute):
            requests.post(
                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Tomorrow%20tasks.json?auth=' + self.id_token,
                data=task)
        else:
            if int(datetime.now().hour) > int(hour):
                requests.post(
                    'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Tomorrow%20tasks.json?auth=' + self.id_token,
                    data=task)
            else:
                try:
                    self.task = SetTask(data_1=name, data_2=time)
                    requests.post(
                        'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Today%20Task.json?auth=' + self.id_token,
                        data=task)
                    origin.add_widget(self.task)
                except Exception as e:
                    print(e)
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    pass


        if repeats == "Once a Month":
            repeat = '{"Name":"' + str(name) + '","Time":"' + str(time) + '","Date":"' + str(datetime.now().day) + '"}'
            requests.post(
                'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Repeats/Once%20a%20Month.json?auth=' + self.id_token,
                data=repeat)
        else:
            if repeats == "Once a Week":
                repeat = '{"Name":"' + str(name) + '","Time":"' + str(time) + '","Date":"' + str(
                    datetime.now().weekday()) + '"}'
                requests.post(
                    'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Repeats/Once%20a%20Week.json?auth=' + self.id_token,
                    data=repeat)
            else:
                if repeats == "Daily":
                    repeat = '{"Name":"' + str(name) + '","Time":"' + str(time) + '"}'
                    requests.post(
                        'https://todo-list-737ca.firebaseio.com/' + self.local_id + '/Repeats/Daily.json?auth=' + self.id_token,
                        data=repeat)
        try:
            done, delete = self.task.response()
            print(delete)
            self.DeleteDone.append(delete)
            print(self.DeleteDone)
            if self.current % 2 == 0:
                self.DeleteDone[self.current].bind(on_release=lambda a, name_task=name,
                                                                     time_task=time: self.DeleteTask(a, self.task,name_task,
                                                                                                     time_task))
                self.current += 1
            self.DeleteDone.append(done)
            if self.current % 2 != 0:
                self.DeleteDone[self.current].bind(
                    on_release=lambda a, name_task=name, time_task=time: self.DoneTask(
                        a, self.task, name_task, time_task))
                self.current += 1
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            pass


    def IstoricFill(self):
        try:
            self.request = requests.get(self.adress)
            self.data = json.loads(self.request.content.decode())
            o = self.root.ids['istoric_screen'].ids['istoric_fill']
            dates = self.data['History']
            ok = 1

            def ShowTasks(button, events):
                InformativePopup(information=events["Events"])

            for i in dates:
                istoric = Button(text=dates[i]["Date"], color=kivy.utils.get_color_from_hex("#ffff00"),
                                 background_color=kivy.utils.get_color_from_hex("#0000ff"),
                                 pos_hint={"center_x": 0.5, "center_y": 0.85 - 0.1 * ok},
                                 size_hint=(0.9, 0.1))
                istoric.bind(on_release=lambda button, date=dates[i]: ShowTasks(button, date))
                o.add_widget(istoric)
                ok += 1
        except:
            pass

    def ShowFriends(self):
        self.request = requests.get(self.adress)
        self.data = json.loads(self.request.content.decode())
        friends = self.data["Friends"]
        InformativePopup(information=friends)

    def AddFriends(self, friend_id):
        check = requests.get('https://todo-list-737ca.firebaseio.com/.json?orderBy="ID"')
        data = check.json()

        for i in data:
            if data[i]["ID"] == friend_id:
                self.root.ids['addfriend_screen'].ids['id_error'].text = str(data[i]["Name"]) + " added as a friend"
                friends = self.data["Friends"]
                friends += str(data[i]["Name"]) + "-" + str(data[i]["ID"])+"-"
                add_friend = '{"Friends":"%s"}' % friends
                try:
                    requests.patch(self.adress, data=add_friend)
                except:
                    pass

    def SelectSound(self, sound):
        alarm = SoundLoader.load('alarm_sounds/' + sound.text + ".mp3")
        sound_alarm = sound.text + ".mp3"
        try:
            requests.patch(self.adress, data='{"Alarm":"' + sound_alarm + '"}')
        except:
            pass
        alarm.play()
        for i in range(5):
            time.sleep(1)
        alarm.stop()


MainApp().run()
