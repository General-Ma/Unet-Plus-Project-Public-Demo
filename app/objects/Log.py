import os
import getpass
from datetime import datetime

class Log(str):
    def __init__(self):
        self.create_at = datetime.now()
        self.os_info = os.name
        self.username = getpass.getuser()
        self.content = ""
    def update(self,string):
        now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        self.content = self.content +now+" "+string+"\n"
    def __str__(self):
        return "created_at: " + str(self.create_at) + "\nos_info: " + self.os_info +  "\nusername: " + self.username + "\ncontent: \n" + self.content
    def __repr__(self):
        return "Log(create_at=" + repr(self.create_at) + ", os_info=" + repr(self.os_info) + ", username=" + repr(self.username) + ", content=" + repr(self.content) + ")"