import kivy
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
from kivy.uix.popup import Popup
import socket; socket.getaddrinfo("google.com", None, socket.AF_INET)

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Game').get_worksheet(0)
sheet1 = client.open('Game').get_worksheet(1)
sheet2 = client.open('Game').get_worksheet(2)
sheetDoHun = client.open('Game').get_worksheet(3)
sheetDareHun = client.open('Game').get_worksheet(4)
sheetDoEng = client.open('Game').get_worksheet(5)
sheetDareEng = client.open('Game').get_worksheet(6)
sheetDoDrink = client.open('Game').get_worksheet(7)
sheetDareDrink = client.open('Game').get_worksheet(8)


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

class DoDPop(Popup):
    def __init__(self, **kwargs):
        self.caller = kwargs.pop('caller')
        super(DoDPop, self).__init__(**kwargs)
    def on_open(self):
        self.background = 'transp.png'


class Card(Screen):
    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.icons = ['pencil_col.png','mouth_col.png','show.png']
        self.i = ''
        self.lang = 'eng'
        self.inpLang = 'eng'

        self.back = (0.4,0,0,1)
        # self.root = activityApp()

    def drawCard(self):
        if self.lang == 'hun':
            data = sheet.col_values(1)
        elif self.lang == 'eng':
            data = sheet1.col_values(1)
        elif self.lang == 'drink':
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
        if self.inpLang == 'hun':
            sheet.insert_row([text], 1)
        elif self.inpLang == 'eng':
            sheet1.insert_row([text], 1)
        elif self.inpLang == 'drink':
            sheet2.insert_row([text], 1)

class DoOrDare(Screen):
    def __init__(self, **kwargs):
        super(DoOrDare, self).__init__(**kwargs)
        self.lang = 'eng'
        self.inpLang = 'eng'
        self.inpCat = 'do'

    def doButton(self):
        if self.lang == 'hun':
            data = sheetDoHun.col_values(1)
        elif self.lang == 'eng':
            data = sheetDoEng.col_values(1)
        elif self.lang == 'drink':
            data = sheetDoDrink.col_values(1)

        self.ids.task.text = random.choice(data)

    def dareButton(self):
        if self.lang == 'hun':
            data = sheetDareHun.col_values(1)
        elif self.lang == 'eng':
            data = sheetDareEng.col_values(1)
        elif self.lang == 'drink':
            data = sheetDareDrink.col_values(1)

        self.ids.task.text = random.choice(data)

    def add(self):
        popup = DoDPop(caller = self)
        popup.open()

    def addTask(self,text):
        if self.inpCat == 'do':
            if self.inpLang == 'hun':
                sheetDoHun.insert_row([text], 1)
            elif self.inpLang == 'eng':
                sheetDoEng.insert_row([text], 1)
            elif self.inpLang == 'drink':
                sheetDoDrink.insert_row([text], 1)
        else:
            if self.inpLang == 'hun':
                sheetDareHun.insert_row([text], 1)
            elif self.inpLang == 'eng':
                sheetDareEng.insert_row([text], 1)
            elif self.inpLang == 'drink':
                sheetDareDrink.insert_row([text], 1)

class activityApp(MDApp):
    def build(self):
        return Manager()

if __name__ =="__main__":
    activityApp().run()
