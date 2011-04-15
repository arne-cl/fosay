# -*- coding: utf-8 -*-
__author__ = "zoltan kochan"
__date__ = "$28 june 2010 1:02:10$"
__name__ = "fosay translator"
__version_info__ = ("pre-alpha", 0, 0, 1, 212)
__version__ = '.'.join([str(i) for i in __version_info__[1:]])

#testing
import test.core.__init__

#notes
#THERE CAN BE A SITUATION LIKE "HARDLY BIG AND SMART" OR "BEAUTIFUL DOG AND CAT"
#PRESENT CONDITIONAL IS ACTUALLY PRESENT OR FUTURE
##DO FOR CHYSLIVNYKY
#'two beatiful girl' is incorrect!!!
#
#from _tkinter import *

#import core.compilers.atnl as atnl
#atnl.parse("number -> gender")
#print(atnl.res)


#TODO: maybe it's wise to drop the gender for pronouns. because I can't save this info with lojban pronouns?!
#TODO: It's better to recognize hun words by analyzing them

#from ftplib import Error

#from platform_info import command
#####from tkinter.constants import VERTICAL
#####from operator import itemgetter
#####from core.lang.scoring import *
#from copy import copy
#from consts import *

#from Microsoft import *

#from sys import setdefaultencoding
#reload(sys)
#
#import Tkinter

#from datetime import datetime

#TODO: nőét nődet etc.

##for key in ukr.vocabulary.keys():
##    print ukr.vocabulary[key][0], ukr.vocabulary[key][0].descr() #, ukr.vocabulary[w][0].meaning
#-------------------------------------------------------------------------------
#ww = [w for w in ukr.vocabulary]
#ww.sort()
#for w in ww:
#    print(w) #, ukr.vocabulary[w][0].meaning
#-------------------------------------------------------------------------------

from core.models.lang import Language
import os, glob, sys

def load_languages():
    curr = str(os.path.dirname(sys.argv[0]))
    path = os.path.join(os.path.join(curr, "data"), "languages.txt")
    f = open(path, encoding = 'utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        sn, ln = line.split(', ')
        yield sn.strip(), ln.strip()

langs = {}
long_names = {}
for sn, ln in load_languages():
    langs[sn] = Language(sn)
    long_names[sn] = ln
    print("%s dictionary has been loaded (%d words; %d meanings)." % (ln, len(langs[sn].vocabulary), len(langs[sn].meanings)))

#hun = Language("hun")
#print("Hungarian dictionary has been loaded (%d words; %d meanings)." % (len(hun.vocabulary), len(hun.meanings)))
#eng = Language("eng")
#print("English dictionary has been loaded (%d words; %d meanings)." % (len(eng.vocabulary), len(eng.meanings)))
#ukr = Language("ukr")
#print("Ukrainian dictionary has been loaded (%d words; %d meanings)." % (len(ukr.vocabulary), len(ukr.meanings)))
#ww = [w for w in ukr.vocabulary]
#ww.sort()
#for w in ww:
#    print(w) #, ukr.vocabulary[w][0].meaning

#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
##JUST TO CHACK#JUST TO CHACK#JUST TO CHACK#JUST TO CHACK#JUST TO CHACK#JUST TO CHACK#JUST TO CHACK#JUST TO CHACK#JUST TO
#import sys
#import os
#
#def save_words(file_name, lang):
#    f = open(str(os.path.dirname(sys.argv[0])) + "\\data\\" + file_name + "\\temp.txt", mode='w', encoding = 'utf-8')
#    ww = [w for w in lang.vocabulary]
#    #ww = [w + " " + str(len(lang.vocabulary[w])) + " " + str([x.descr() for x in lang.vocabulary[w]]) for w in lang.vocabulary]
#    ww.sort()
#    for w in ww:
#        f.write(w + "\n") #, ukr.vocabulary[w][0].meaning
#    f.close()
#
#save_words("hun", hun)
#save_words("eng", eng)
#save_words("ukr", ukr)
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################




#PARTICIPLE SHOULD BE AN ENUM. LIKE ALL PROPS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#text = "A boy saw a beautiful house and a smart girl."; source_lang = eng; first = "ip" #doesn't work
#text = "A boy saw a house and a girl."; source_lang = eng; first = "ip" #doesn't work
#text = "The boy saw the house."; source_lang = eng; first = "ip"
#text = "The sibling saw the house."; source_lang = eng; first = "ip"
#text = "He saw the house."; source_lang = eng; first = "ip"
#text = "Ivan saw the house."; source_lang = eng; first = "ip"
#text = "The boys saw a woman in the house."; source_lang = eng; first = "ip"
#text = "The boy and the girl saw a woman."; source_lang = eng; first = "ip"
#text = "The boy saw a house in the house."; source_lang = eng; first = "ip"
#text = "The smart boy saw the beautiful girl in the beautiful house."; source_lang = eng; first = "ip"
#text = "The smart boy saw the beautiful woman and the woman in the house."; source_lang = eng; first = "ip"
#text = "The boy will see the woman in the house."; source_lang = eng; first = "ip"
#text = "in the house"; source_lang = eng; first = "INOBJ"
#text = "A boy saw a house."; source_lang = eng; first = "ip"
#text = "The boy has seen the house."; source_lang = eng; first = "ip"
#text = "A boy see a house."; source_lang = eng; first = "ip" #incorrect!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#text = "The boy sees the house."; source_lang = eng; first = "ip"
#text = "A boy did see a house."; source_lang = eng; first = "ip"
#text = "A boy does see a house."; source_lang = eng; first = "ip"
#text = "A boy will see a house."; source_lang = eng; first = "ip"
#text = "The woman is seeing the house."; source_lang = eng; first = "ip"
#text = "The boy has been seeing a house and a woman."; source_lang = eng; first = "ip"
#text = "I see you."; source_lang = eng; first = "ip"
#text = "The boy is going into the house."; source_lang = eng; first = "ip"
#text = "The boy was going to the school."; source_lang = eng; first = "ip"
#text = "a house of a woman"; source_lang = eng; first = "NP"
#text = "A boy saw a woman's house."; source_lang = eng; first = "ip"
#text = "A woman's house saw a boy."; source_lang = eng; first = "ip"
#text = "The house of the woman saw a boy."; source_lang = eng; first = "ip"
#text = "A house of the woman saw a boy."; source_lang = eng; first = "ip"
#text = "The woman's house saw a boy."; source_lang = eng; first = "ip"
#text = "the house of the woman"; source_lang = eng; first = "OBJ"
#text = "The boy will see the woman's house."; source_lang = eng; first = "ip"
text = "Today the boy will see the house of the woman."; source_lang = langs['eng']; first = "ip"
#text = "The boy will see a house in Uzhhorod."; source_lang = eng; first = "ip"
#text = "Today Ivan will see Yuliya's house in Uzhhorod."; source_lang = eng; first = "ip"
#text = "Today Ivan will see all houses of Yulia in Uzhhorod."; source_lang = eng; first = "ip" #was/is working bad coz of difinity passin, referencing...
#text = "Once upon a time the boy saw the woman's house."; source_lang = eng; first = "ip"
#text = "John saw a house."; source_lang = eng; first = "ip"
#text = "a house"; source_lang = eng; first = "np"
#print(eng.atn['np'])
#text = "Yulia saw a house."; source_lang = eng; first = "ip"
#text = "Yulia has been seeing a house."; source_lang = eng; first = "ip"

#text = "Хлопець бачив жінку."; source_lang = ukr; first = "ip"
#text = "Хлопець бачив дівчину."; source_lang = ukr; first = "ip"
#text = "Іван бачив жінку."; source_lang = ukr; first = "ip"
#text = "Іван жінку бачив."; source_lang = ukr; first = "ip"
#text = "Іван гарного будинок бачив."; source_lang = ukr; first = "ip" #НЕ МАЄ РОБИТИ
#text = "Іван гарний будинок бачив."; source_lang = ukr; first = "ip"
#text = "Хлопець і дівчина бачили жінку."; source_lang = ukr; first = "ip"
#text = "Сестра або брат бачили будинок."; source_lang = ukr; first = "ip"
#text = "Сестра або брат бачать будинок."; source_lang = ukr; first = "ip"
#text = "Сестра побачила будинок."; source_lang = ukr; first = "ip"
#text = "Сестра бачить будинок."; source_lang = ukr; first = "ip"
#text = "Хлопець бачитиме жінку."; source_lang = ukr; first = "ip" #latni FOGJA!!!
#text = "Бачитиме хлопець жінку в будинку."; source_lang = ukr; first = "IP
#text = "Хлопці бачили жінку в будинку."; source_lang = ukr; first = "ip"
#text = "Хлопець бачить."; source_lang = ukr; first = "ip"
#text = "Хлопець і дівчина бачать."; source_lang = ukr; first = "ip"
#text = "Хлопець і дівчина бачать жінку."; source_lang = ukr; first = "ip"
#text = "хлопець і дівчина"; source_lang = ukr; first = "NP"
#text = "Бачитиме хлопець жінку в будинок."; source_lang = ukr; first = "ip"
#text = "Бачитиме гарний хлопець жінку в будинку."; source_lang = ukr; first = "ip"
#text = "Бачитиме хлопець жінку з гарного будинку."; source_lang = ukr; first = "ip" #гарного
#text = "Бачитиме хлопчик жінку з будинку."; source_lang = ukr; first = "ip" #гарного
#text = "з будинку"; source_lang = ukr; first = "ELOBJ" #гарного
#text = "Хлопчик бачитиме жінки будинок."; source_lang = ukr; first = "ip" #TODO: It is not working!
#text = "Бачитиме хлопчик жінки будинок."; source_lang = ukr; first = "ip" #TODO: I SHOULD ADD IT TO THE TESTS!!! I SHOULD ADD IT TO THE TESTS!!! I SHOULD ADD IT TO THE TESTS!!!
#text = "Я бачив тебе."; source_lang = ukr; first = "ip"
#text = "Бачу тебе."; source_lang = ukr; first = "ip" #THERE ARE IDENTIC. CASEFRAMES BECAUSE "тебе" HAS DIFFERENT GENDERS
#text = "Чувак бачив дівчину."; source_lang = ukr; first = "ip"
#text = "Хлопець бачив дівчину."; source_lang = ukr; first = "ip" #MAKE FOR HUNGARIAN
#text = "Кожний хлопець бачив кожну дівчину."; source_lang = ukr; first = "ip"
#text = "Кожний хлопець бачив дівчину."; source_lang = ukr; first = "ip"
#text = "Усі хлопці бачили дівчат."; source_lang = ukr; first = "ip"
#text = "Декілька хлопців бачили декількох дівчат."; source_lang = ukr; first = "ip"
#text = "Декілька хлопців бачили дівчат."; source_lang = ukr; first = "ip"
#text = "Всі хлопці бачили багатьох дівчат."; source_lang = ukr; first = "ip"
#text = "Кожен хлопець бачив багатьох гарних і розумних дівчат."; source_lang = ukr; first = "ip"
#text = "Хлопець бачитиме дівчат і жінок."; source_lang = ukr; first = "ip"
#text = "Хлопець і дівчина бачитимуть жінку."; source_lang = ukr; first = "ip"
#text = "Кожен хлопець бачив багатьох гарних, розумних дівчат."; source_lang = ukr; first = "ip"


#text = "Iván látta a nőnek a házát."; source_lang = hun; first = "ip"
#text = "Iván látta a házat."; source_lang = hun; first = "ip"
#text = "Iván látta a szép házat."; source_lang = hun; first = "ip"
#text = "Egy fiú látta a házat."; source_lang = hun; first = "ip"
#text = "A fiú és a lány látták a nőt."; source_lang = hun; first = "ip"
#text = "Egy fiú és egy lány láttak egy házat."; source_lang = hun; first = "ip"
#text = "Egy fiú látta egy okos nő szép házát."; source_lang = hun; first = "ip"
#text = "A fiú látta egy okos nőnek a szép házát."; source_lang = hun; first = "ip" #egy okos n''o f'erje h'az'at!!!'
#egy okos nő férjének a házát
#text = "egy nőnek"; source_lang = hun; first = "POSS1"
#text = "egy nőnek a háza"; source_lang = hun; first = "NP"
#text = "A házat a fiú meglátta."; source_lang = hun; first = "ip"
#text = "Én látlak téged."; source_lang = hun; first = "ip"
#text = "Látlak."; source_lang = hun; first = "ip"
#text = "Látok."; source_lang = hun; first = "ip"
#text = "Én láttam téged."; source_lang = hun; first = "ip" #should not build parse tree for it!
#text = "Néhány fiú látott egy házat."; source_lang = hun; first = "ip"
#text = "Néhány fiú látott sok szép házat."; source_lang = hun; first = "ip" #WIERD TRANSLATION TO UKR 'COZ OF EXTRA1!!!!!
#text = "Néhány fiú látott sok szép lányt."; source_lang = hun; first = "ip"


#text = "Látlak téged."; source_lang = hun; first = "ip" #should not build parse tree for it!
#text = "Én látlak."; source_lang = hun; first = "ip" #should not build parse tree for it!

target_langs = [langs[key] for key in langs.keys() if not langs[key] == source_lang]


#params####################

from core.lang.translate import translate, text_to_interlingua, interlingua_to_str

#import sys
#from PyQt4 import QtGui
#app = QtGui.QApplication(sys.argv)
#
#widget = QtGui.QWidget()
#widget.resize(250, 150)
#widget.setWindowTitle('simple')
#widget.show()
#
#sys.exit(app.exec_())

from idlelib.PyShell import tkMessageBox

translations = translate(text, first, source_lang, target_langs)

shift = 3 * " "
UC = 35
pr = "translating:\n" #print("translating:")
pr += shift + text + "\n" #print(shift + text)
pr += UC*"_" + "\n" #print(40*"=")
i = 0
for l in target_langs:
    pr += "translating to " + str(l) + ":\n" #; ln += 1 #print("translating #" + str(ln) + ":"); ln += 1
    for item in translations[i]:
        pr += shift + str(item) + "\n"
    i += 1

tkMessageBox.showinfo("FOSAY translator", pr)










import tkinter; from tkinter import *
from tkinter import ttk

class TranslatorFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")
        self.parent = parent
        self.initialize()

    def initialize(self):
        #init Frame
        self.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        #init source_text
        self.source_text = Text(self, width=100, height=15, font=11)
        #self.source_text.pack(anchor=NE)
        self.source_text.grid(sticky=E+W)
        self.source_text.focus_set()

#        #init source_scrollbar
#        self.source_scrollbar = ttk.Scrollbar(self.parent, orient=VERTICAL)
#        #self.source_scrollbar.pack(side=RIGHT, fill=Y)
#        self.source_scrollbar.configure(command=self.source_text.yview)
#        self.source_text.configure(yscrollcommand=self.source_scrollbar.set)

        #init source_combo_box
        self.source_combo_box = ttk.Combobox(self, state="readonly", font=11)
        self.source_combo_box.config(width=10)
        self.source_combo_box.grid(row=16, sticky=W)
        self.source_combo_box['values'] = [key for key in long_names.values()]

        #init translate_button
        self.translate_button = ttk.Button(self, text=">>", command=self.trans)
        self.translate_button.config(width=10)
        self.translate_button.grid(row=17, sticky=W)

        #init target_combo_box
        self.target_combo_box = ttk.Combobox(self, state="readonly", font=11)
        self.target_combo_box.config(width=10)
        self.target_combo_box.grid(row=18, sticky=W)
        self.target_combo_box['values'] = [key for key in long_names.values()] + ["interlingua"]

        #init target_text
        self.target_text = Text(self, width=80, height=10, font=11)
        self.target_text.config(state=DISABLED)
        #self.target_text.pack(anchor=S)
        self.target_text.grid(sticky="EW")

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

    def trans(self):
        srclan = langs[self.source_combo_box.get()]
        text = self.source_text.get('1.0', 'end').strip()
        first = 'ip'
        self.target_text.config(state=NORMAL)
        self.target_text.delete('1.0', 'end')
        if self.target_combo_box.get() == "interlingua":
            s = interlingua_to_str(text_to_interlingua(text, first, srclan)[0])
            self.target_text.insert('end', s)
        else:
            trglan = langs[self.target_combo_box.get()]
            tr = translate(text, first, srclan, [trglan])
            self.target_text.insert('end', tr)
        self.target_text.config(state=DISABLED)




#feet_entry.focus()
#root.bind('<Return>', calculate)

root = Tk()
root.title("fosay translator " + __version_info__[0] + " " + __version__)
tf = TranslatorFrame(root)
root.mainloop()
