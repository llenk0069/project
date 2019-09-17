import socket
import threading
from base64 import b64encode
from hashlib import sha1
import struct
import sys
from functools import lru_cache
from urllib.parse import parse_qs, urlparse
from model import Wall
import json
from datetime import datetime
wall = Wall()
MAX_LEN = 64*1024

class ClientRequestHandler:
    def __init__(self,sock):
        self.socket = sock
        self.rfile = sock.makefile('rb')
        self.keepwork = 1

    def handshake_fn(self):
            headers= {}
            while True:
                header = self.rfile.readline().decode().strip()
                if not header:
                    break
                head , value = header.split(':',1)
                headers[head.lower().strip()]=value.strip()
            self.headers = headers




    def parse_request(self):
        buf = ''

        self.raw = self.rfile.readline(MAX_LEN+1)
        if len(self.raw)==0:
            return
        else:
            if len(self.raw) > MAX_LEN:
                raise Exception('Request line is too long')

            req_line = str(self.raw, 'iso-8859-1')
            req_line = req_line.rstrip('\r\n')
            words = req_line.split()
            print(words)
            self.method, target, ver = words
            self.url = urlparse(target)
            self.path = self.url.path
            #self.query = parse_qs(self.url.query)
            

    def send_response(self, status, reason, headers=None, body=""):

        self.wfile = self.socket.makefile('wb')
        status_line  = 'HTTP/1.1 {} {}\r\n'.format(status, reason)
        status_line += 'Version: HTTP/1.1\r\n'
        status_line += 'Content-Type: application/json; charset=utf-8\r\n'
        status_line += 'Content-Length: {}'.format(len(body))
        status_line += "\r\n\r\n"
        status_line += body

        self.wfile.write(status_line.encode())
        self.wfile.close()
        self.socket.close()

    def handle_request(self):
        if self.path == '/users/add' and self.method == 'POST':
            return self.add_users()

        if self.path == '/chats/add' and self.method == 'POST':
            return self.add_chat()

        if self.path == '/messages/add' and self.method == 'POST':
            return self.add_message()

        if self.path == '/chats/get' and self.method == 'POST':
            return self.get_chats()

        if self.path == '/messages/get' and self.method == 'POST':
            return self.get_messages()

        else:
            self.send_response(400,'broken data')

    def body(self):
        if 'content-length' in self.headers:
            size = int(self.headers.get('content-length'))
            if not size:
                return None
            self.body =  self.rfile.read(size).decode()
            if self.headers.get('content-type') == 'application/json' :
                try:
                    self.body = json.loads(self.body)
                except json.decoder.JSONDecodeError:
                    pass
        else:
            return None


    def add_users(self):

        if type(self.body) == dict and "username" in self.body:
            user_name = self.body['username']
            if wall.register(user_name):
                self.send_response(201, 'Created')
            else:
                self.send_response(204, 'NoCreated')
        else:
            self.send_response(400,'broken data')


    def add_chat(self):
        if type(self.body)==dict and "name" and "users" in self.body:
            chat_name = self.body['name']
            users = self.body['users']
            if wall.new_chat(chat_name,users):
                self.send_response(201, 'Created')
            else:
                self.send_response(204, 'NoCreated')
        else:
            self.send_response(400,'broken data')

    def add_message(self):
        if type(self.body)==dict and "chat" and "author" and "text" in self.body:
            chat_id = self.body['chat']
            author = self.body['author']
            text = self.body['text']
            print(chat_id, author, text)
            if wall.message(chat_id, author, text):
                self.send_response(201, 'Created')
            else:
                self.send_response(204, 'NoCreated')
        else:
            self.send_response(400,'broken data')

    def get_chats(self):
        if type(self.body)==dict and "user" in self.body:
            user_id= str(self.body['user'])
            t= wall.user_all_chats(user_id)
            t = wall.sort_message_by_time(t)
            resp_body=""
            for i in t:
                resp_body+=json.dumps(i)+"\r\n"
            self.send_response(200, 'getted', body=resp_body)

        else:
            self.send_response(400,'broken data')

    def get_messages(self):
        if type(self.body)==dict and "chat" in self.body:
            chat_id= str(self.body['chat'][0])
            t= wall.get_chat_messages(chat_id)
            t = wall.sort_message_by_time(t)
            resp_body=""
            for i in t:
                resp_body+=json.dumps(i)+"\r\n"
            self.send_response(200, 'getted', body=resp_body)

        else:
            self.send_response(400,'broken data')

    def work(self):
            self.parse_request()
            if len(self.raw)>0:
                self.handshake_fn()
                self.body()
                self.handle_request()
                sys.exit()





def new_client(sock):
    client = ClientRequestHandler(sock)
    client.work()

def server_run():
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_socket.bind(("localhost",9000))
    serv_socket.listen()
    cid = 0
    while True:
        client_sock, client_addr = serv_socket.accept()
        t = threading.Thread(target=new_client, args=(client_sock,))
        t.start()


server_run()
