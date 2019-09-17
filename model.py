#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import time
from time import gmtime, strftime, localtime
from datetime import datetime
class Wall:
    USERS = 'users.json'
    CHATS = 'chats.json'
    MESSAGES = 'messages.json'

    def time_to_unix(self, str_time):
        t = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        return t.timestamp()

    def sort_message_by_time(self,arr=[]):
        arr.sort(key = lambda x: self.time_to_unix(x['time']))
        return(arr)

    def get_time(self):
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

    def __init__(self):
        try:
            with open(self.USERS, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.USERS, 'w', encoding='utf-8') as f:
                json.dump({"users":[], "id_count":0}, f)

        try:
            with open(self.MESSAGES, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.MESSAGES, 'w', encoding='utf-8') as f:
                json.dump({"messages":{}, "id_count":0}, f)

        try:
            with open(self.CHATS, 'r', encoding='utf-8'):
                pass
        except FileNotFoundError:
            with open(self.CHATS, 'w', encoding='utf-8') as f:
                json.dump({"chats":[], "id_count":0}, f)

    def register(self, user):
        if self.find_by_name(user):
            return False  # Такой пользователь существует
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        users['id_count']+=1
        user={"id":users['id_count'], "name":user, "time":self.get_time()}
        users['users'].append(user)
        with open(self.USERS, 'w', encoding='utf-8') as f:
            json.dump(users, f)
        return True

    def message(self, chat_id, user_id, text):
        with open(self.MESSAGES, 'r', encoding='utf-8') as f:
            messages = json.load(f)
            messages["id_count"]+=1
            messages["messages"][str(messages["id_count"])]={"chat":str(chat_id), "author":str(user_id),"time":self.get_time(),"text":text}
            with open(self.MESSAGES, 'w', encoding='utf-8') as f:
                json.dump(messages, f)
            return True

    def new_chat(self, name, users=[]):
        with open(self.CHATS, 'r', encoding='utf-8') as f:
            chats = json.load(f)
            chats["id_count"]+=1
            chat={"name":name, "users":users, "time":self.get_time(), "id":chats['id_count']}
            chats['chats'].append(chat)
            with open(self.CHATS, 'w', encoding='utf-8') as f:
                json.dump(chats, f)
            return True

    def append_user(self,chat_id, user_id):
        with open(self.CHATS, 'r', encoding='utf-8') as f:
            chats = json.load(f)
            chats["chats"][str(chat_id)]['users'].append(str(user_id))
            with open(self.CHATS, 'w', encoding='utf-8') as f:
                json.dump(chats, f)



    def find(self,user_name):
        user = self.find_by_name(user_name)
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        if (password==user['password']):
            print('ok')
            return True
        return False

    def find_by_name(self,user):
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        for i in users['users']:
            if i['name']==user:
                return True

    def find_by_id(self,user_id):
        with open(self.USERS, 'r', encoding='utf-8') as f:
            users = json.load(f)
        for i in users['user']:
            if i['id']==user_id:
                return i

    def user_all_chats(self,user_id):
        user_chats = []
        user_id = str(user_id)
        with open(self.CHATS, 'r', encoding='utf-8') as f:
            chats = json.load(f)
            for i in chats["chats"]:
                if user_id in i["users"]:
                   user_chats.append(i)
            return user_chats

    def get_chat_messages(self,chat_id):
        chat_messages= []
        with open(self.MESSAGES, 'r', encoding='utf-8') as f:
            messages = json.load(f)
            for i in messages["messages"]:
                if messages["messages"][i]["chat"]==chat_id:
                    chat_messages.append(messages["messages"][i])
            return(chat_messages)

    def find_chat_by_id(self,chat_name):
        with open(self.CHATS, 'r', encoding='utf-8') as f:
            chats = json.load(f)
            for i in chats["chats"]:
                if [i]['id']==chat_name:
                    return int(i)

    def sort_message_by_time(self,arr=[]):
        arr.sort(key = lambda x: self.time_to_unix(x['time']))
        return(arr)
