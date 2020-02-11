import kivy
kivy.require('1.9.1')

# add the following 2 lines to solve OpenGL 2.0 bug
from kivy import Config
Config.set('graphics', 'multisamples', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from pathlib import Path
import os,os.path
import email
import mysql.connector
import operator

emailFolder = "C:/Users\Ahmad Naeem Khokhar/Downloads/Video/Compressed/enron_mail_20150507/maildir"

#getting all the paths of emal
allDocs = Path(emailFolder).glob("**/*")

files=[]
for x in allDocs:
    if len(files)<50000:
        if x.is_file():
            files.append(x)
    else:
    	break
# count for next and previous emails to show
s_index=0
indexDocs= [432,234,565,789,999,123,654,765,333,456,242]

#reading database
conn = mysql.connector.connect(user="root", password = "mankhokhar", host = "localhost")
cursor = conn.cursor()



# accessing database
conn = mysql.connector.connect(user="root", password = "mankhokhar", host = "localhost")
cursor = conn.cursor()

searcher=dict()
count=dict()

def getFromDB(word):
    cursor.execute("use mission_enron;")
    cursor.execute("""select Doc_id_B, Word_Count_ from rev_index_body where Word_B like "%s";""" % (word))
    retrived=cursor.fetchall()

    for i in retrived:
        if i[0] in searcher.keys():
            searcher[i[0]] +=i[1]
            count[i[0]]+=1
        else:
            searcher[i[0]] =i[1]
            count[i[0]]=1


    cursor.execute("""select Doc_id, Word_Count from rev_index_subject  where Word like "%s";""" % (word))
    retrived=cursor.fetchall()

    for i in retrived:
        if i[0] in searcher.keys():
            searcher[i[0]] +=i[1]
            count[i[0]]+=1
        else:
            searcher[i[0]] =i[1]
            count[i[0]]=1

def searchResults():
    dictionaryKEY=[]
    for i in searcher.items():
    ##print(i[0], i[1], count[i[0]])
        searcher[i[0]] = i[1] * count[i[0]]

    for i in sorted(searcher.items(), key=operator.itemgetter(1),reverse=True):
        dictionaryKEY.append(i[0])
	searcher.clear()
	count.clear()

    return dictionaryKEY[0:11]

def read_file(index):
		eachFile = files[index]
		myFile = open(eachFile,'r')
		emailData = myFile.read()
		tempEmail = email.message_from_string(emailData)
		tempSender = str(tempEmail['from'])
		tempReciever = str(tempEmail['to'])
		tempSubject = str(tempEmail['subject'])
		tempDate = str(tempEmail['date'])
		tempMessage = tempEmail.get_payload(decode = True)
		
    	#if email has multiple parts like images etc
		if tempEmail.is_multipart():
			for part in tempEmail.walk():
					ctype = part.get_content_type()
					cdispo = str(part.get('Content-Disposition'))

					if ctype == 'text/plain' and 'attachment' not in cdispo:
							tempMessage = part.get_payload(decode = False)
							break
		else:
			tempMessage = tempEmail.get_payload(decode = False)
		tempMessage = str(tempMessage)
		em =  tempDate+ "\n" + tempSender + "\n" + tempSubject + "\n" + tempMessage + "\n"
		return em




class HomePage(Screen):
    pass
class SearchPage(Screen):
    pass

class ScreenManagement(ScreenManager):
	pass

project1 = Builder.load_file('MissionEnron.kv')
    
class Mission(App):

	def search(self,txt):
		global indexDocs
		global s_index
		s_index = 0
		getFromDB(txt)
		indexDocs = searchResults()
		print(indexDocs)

	def build(self):
		return project1

	def next_file(self):
		global s_index
		if s_index < 10:
			s_index += 1
		elif s_index >= 10:
			s_index = 0
		print(s_index)
		file = read_file(indexDocs[s_index])
		return file


	def back_file(self):
		global s_index
		if s_index > 0:
			s_index -= 1
		elif s_index <= 0:
			s_index = len(indexDocs) - 1
		print(s_index)
		file = read_file(indexDocs[s_index])
		return file

	def get_e_index(self):
		global s_index
		return str(s_index) + " out of " +str(len(indexDocs) -1)


if __name__ == '__main__':
	Mission().run()
