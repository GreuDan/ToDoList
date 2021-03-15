import json
import requests
from kv.settask import SetTask
def DeleteTask(a, widget, name, time,delete_task):
    delete_task.request = requests.get(delete_task.adress)
    data = json.loads(delete_task.request.content.decode())
    try:
        dates = data['Today Task']
        for i in dates:
            if dates[i]["Name"] == str(name) and dates[i]["Time"] == str(time):
                try:
                    a1 = 0
                    requests.delete(
                        'https://todo-list-737ca.firebaseio.com/' + delete_task.local_id + '/Today%20Task/' + str(
                            i) + '.json?auth=' + delete_task.id_token)
                    widget.DisableButtons(a1)
                except:
                    pass
    except:
        pass


def DoneTask(a,update_done_tasks, widget, name, time):
    update_done_tasks.AccountFill()
    a1 = 1
    Done_now = update_done_tasks.Done_1 + 1
    Done_3 = update_done_tasks.Done_3 + 1
    upd_done = '{"Account": {"Today Tasks": {"Done": "' + str(Done_now) + '", "Undone": "' + str(
        update_done_tasks.Undone_1) + '"}, "Week Tasks": ' \
                         '{"Done": "' + str(Done_3) + '",' \
                                                      ' "Undone": "' + str(
        update_done_tasks.Undone_3) + '"},"Yesterday Tasks": {"Done": "' + str(update_done_tasks.Done_2) + '", "Undone": "' + str(
        update_done_tasks.Undone_2) + '' \
                         '"}}}'
    update_done_tasks.adress = 'https://todo-list-737ca.firebaseio.com/' + update_done_tasks.local_id + '.json?auth=' + update_done_tasks.id_token
    requests.patch(update_done_tasks.adress, data=upd_done)
    try:
        update_done_tasks.request = requests.get(update_done_tasks.adress)
        data = json.loads(update_done_tasks.request.content.decode())
        try:
            dates = data['Today Task']
            for i in dates:
                if dates[i]["Name"] == str(name) and dates[i]["Time"] == str(time):
                    try:
                        data = '{"Name":"' + str(name) + '","Time":"Done"}'
                        requests.delete(
                            'https://todo-list-737ca.firebaseio.com/' + update_done_tasks.local_id + '/Today%20Task/' + str(
                                i) + '.json?auth=' + update_done_tasks.id_token)
                        requests.post(
                            'https://todo-list-737ca.firebaseio.com/' + update_done_tasks.local_id + '/Today%20Task/.json?auth=' + update_done_tasks.id_token,
                            data=data)
                        widget.DisableButtons(a1)
                    except:
                        pass
        except:
            pass
    except:
        pass


def MissTask(update_undone_tasks,name, time):

    Undone_1 = update_undone_tasks.Undone_1 + 1
    Undone_3 = update_undone_tasks.Undone_3 + 1
    upd_undone = '{"Account": {"Today Tasks": {"Done": "' + str(update_undone_tasks.Done_1) + '", "Undone": "' + str(
        Undone_1) + '"}, "Week Tasks": ' \
                    '{"Done": "' + str(update_undone_tasks.Done_3) + '",' \
                                                      ' "Undone": "' + str(
        Undone_3) + '"},"Yesterday Tasks": {"Done": "' + str(update_undone_tasks.Done_2) + '", "Undone": "' + str(
        update_undone_tasks.Undone_2) + '' \
                         '"}}}'
    requests.patch(update_undone_tasks.adress, data=upd_undone)
    update_undone_tasks.AccountFill()
    try:
        update_undone_tasks.request = requests.get(update_undone_tasks.adress)
        data = json.loads(update_undone_tasks.request.content.decode())
        try:
            dates = data['Today Task']
            for i in dates:
                if dates[i]["Name"] == str(name) and dates[i]["Time"] == str(time):
                    try:
                        data_task = '{"Name":"' + str(name) + '","Time":"Miss"}'
                        requests.delete(
                            'https://todo-list-737ca.firebaseio.com/' + update_undone_tasks.local_id + '/Today%20Task/' + str(
                                i) + '.json?auth=' + update_undone_tasks.id_token)
                        requests.post(
                            'https://todo-list-737ca.firebaseio.com/' + update_undone_tasks.local_id + '/Today%20Task/.json?auth=' + update_undone_tasks.id_token,
                            data=data_task)
                        return "Miss"
                    except:
                        pass
        except:
            pass
    except:
        pass