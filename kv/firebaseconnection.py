import requests
import json
from kivy.app import App
import shortuuid
from kivy.uix.screenmanager import  NoTransition, CardTransition


class FirebaseConnection():
    web_api_key="AIzaSyASVKHx6EC6_b7LrhVMmgFiFe0HA2ZpWUg"
    def sign_up(self,email,password,name):
        app=App.get_running_app()
        url="https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key="+self.web_api_key
        data_signup_load={"email":email,"password":password,"returnSecureToken":True}
        data_sign_request=requests.post(url,data=data_signup_load)
        data_sign_up=json.loads(data_sign_request.content.decode())
        if name:
            if data_sign_request.ok == True:
                refresh_token = data_sign_up["refreshToken"]
                localId = data_sign_up["localId"]
                idToken = data_sign_up["idToken"]
                with open("kv/refreshToken.txt", "w") as save_file:
                    save_file.write(refresh_token)
                app.local_id = localId
                app.id_token = idToken
                user_id = "#" + shortuuid.uuid()

                default_data = '{"Alarm":"Fast A1.mp3","Day":"","Account": {"Today Tasks": {"Done": "0", "Undone": "0"}, "Week Tasks": ' \
                               '{"Done": "0", "Undone": "0"},"Yesterday Tasks": {"Done": "0", "Undone": "0"}}, "Email":"' + str(
                    email) + '", "Friends": "", "History": "", "ID": "' + str(user_id) + '", "Name": "' + str(
                    name) + '","Repeats": {"Daily": "", "Once a Month": "", "Once a Week":""},"History":{"Default":{"Name":"Default","Time":"0"}}, "Today Task":{"Default":{"Name":"Default","Time":"0"}}, "Tomorrow tasks":{"Default":{"Name":"Default","Time":"0"}}}'
                user_name = app.root.ids['account_screen'].ids['label_2'].text=str(name)
                userid = app.root.ids['account_screen'].ids['label_4'].text=user_id
                user_email = app.root.ids['account_screen'].ids['label_6'].text=str(email)
                post_request = requests.patch(
                    'https://todo-list-737ca.firebaseio.com/' + localId + '.json?auth=' + idToken, data=default_data)
                app.root.transition = NoTransition()
                app.root.current = "scheduel_screen"
                app.root.transition = CardTransition()

            if data_sign_request.ok == False:
                error = json.loads(data_sign_request.content.decode())
                message_error = error["error"]["message"]
                if message_error == 'INVALID_EMAIL':
                    label_error = app.root.ids['authentification_screen'].ids['email_error']
                    label_error.text = "Please check your email to be correctly written "
                else:
                    if message_error == 'WEAK_PASSWORD : Password should be at least 6 characters':
                        label_error = app.root.ids['authentification_screen'].ids['password_error']
                        label_error.text = "Please enter a strong password "
        else:
            label_error = app.root.ids['authentification_screen'].ids['name_error']
            label_error.text = "Please enter your name"


    def exchange_refresh_token(self,refresh_token):
        url="https://securetoken.googleapis.com/v1/token?key="+self.web_api_key
        refresh_payload='{"grant_type":"refresh_token","refresh_token":"%s"}' % refresh_token
        request=requests.post(url,data=refresh_payload)
        id_token=request.json()["id_token"]
        local_id=request.json()["user_id"]
        return id_token,local_id

