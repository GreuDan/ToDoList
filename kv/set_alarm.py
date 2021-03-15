import requests
import json
from kv.main import MainApp

from kivy.core.audio import SoundLoader
import time
class Sound:
    def __init__(self):
        self.request=MainApp.getRequest()
        self.adress=MainApp.getAdress()
    def SetAlarm(self):
        self.request = requests.get(self.adress)
        data = json.loads(self.request.content.decode())
        alarm = SoundLoader.load('alarm_sounds/' + str(data["Alarm"]))

    def SelectSound(app, sound):
        app.alarm = SoundLoader.load('alarm_sounds/' + sound.text + ".mp3")
        sound_alarm = sound.text + ".mp3"
        try:
            requests.patch(app.adress, data='{"Alarm":"' + sound_alarm + '"}')
        except:
            pass
        app.alarm.play()
        for i in range(5):
            time.sleep(1)
        app.alarm.stop()
