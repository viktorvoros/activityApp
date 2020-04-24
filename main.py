import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.popup import Popup
from kivy.uix.actionbar import ActionBar

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Game').sheet1
sheet2 = client.open('Game').get_worksheet(1)


class Manager(ScreenManager):
    pass

class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)


class WordInput(Screen):
    def addWord(self,text):
        sheet.insert_row([text], 2)
        self.ids.new.text = ''
    pass

class Pop(Popup):
    def __init__(self, **kwargs):
        self.caller = kwargs.pop('caller')
        super(Pop, self).__init__(**kwargs)
    def on_open(self):
        self.background = 'transp.png'


class Card(Screen):
    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.icons = ['pencil_col.png','mouth_col.png','show.png']
        self.i = ''
        self.lang = 1
        self.back = (0.4,0,0,1)
        # self.root = activityApp()

    def drawCard(self):
        if self.lang == 1:
            data = sheet.col_values(1)
        else:
            data = sheet2.col_values(1)
        # print(data)
        self.ids.word.text = random.choice(data)
        self.ids.img.source = random.choice(self.icons)
        # print(self.ids.img.source)
        if self.ids.img.source == 'pencil.png':
            self.back = (0.4,0,0,1)
        if self.ids.img.source == 'mouth.png':
            self.back = (0,0,0.4,1)
        if self.ids.img.source == 'show.png':
            self.back = (0.4,0.4,0,1)

    def add(self):
        popup = Pop(caller = self)
        popup.open()

    def addWord(self,text):
        if self.lang == 1:
            sheet.insert_row([text], 2)
        else:
            sheet2.insert_row([text], 1)
        # Pop.ids.new.text = ''



class activityApp(MDApp):
    def build(self):

        return Manager()

if __name__ =="__main__":
    activityApp().run()
