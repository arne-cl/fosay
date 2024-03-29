__author__ = "zoltan kochan"
__date__ = "$28 june 2010 1:02:10$"
__name__ = "fosay translator"
__version_info__ = ("pre-alpha", 0, 0, 1, 239)
__version__ = '.'.join([str(i) for i in __version_info__[1:]])

#testing
#import test.core.__init__

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
short_name = {}
for sn, ln in load_languages():
    langs[sn] = Language(sn)
    long_names[sn] = ln
    short_name[ln] = sn
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
#    #ww = [w for w in lang.vocabulary]
#    ww = [w + " " + str(len(lang.vocabulary[w])) + " " + str([x.descr() for x in lang.vocabulary[w]]) for w in lang.vocabulary]
#    ww.sort()
#    for w in ww:
#        f.write(w + "\n") #, ukr.vocabulary[w][0].meaning
#    f.close()
#
#save_words("hun", langs["hun"])
#save_words("eng", langs["eng"])
#save_words("ukr", langs["ukr"])
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################


def friendly_output(t):
    if len(t) == 0:
        return """
            THE TRANSLATOR WAS UNABLE TO TRANSLATE THE GIVEN TEXT
            You either made a mistake or it's too hard for the translator yet.
            """
    if len(t) == 1:
        return t[0]
    alt = 1
    out = ""
    for item in t:
        out += "alternative #" + str(alt) + ":\n"
        out += item + "\n\n"
        alt += 1
    return out

from core.lang.translate import translate, text_to_interlingua, interlingua_to_str

try:
    from PyQt4 import QtCore, QtGui

    try:
        _fromUtf8 = QtCore.QString.fromUtf8
    except AttributeError:
        _fromUtf8 = lambda s: s

    class Ui_FosayForm(object):
        def setupUi(self, FosayForm):
            FosayForm.setObjectName(_fromUtf8("FosayForm"))
            FosayForm.resize(294, 438)
            self.gridLayout = QtGui.QGridLayout(FosayForm)
            self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
            self.sourceTextEdit = QtGui.QTextEdit(FosayForm)
            self.sourceTextEdit.setObjectName(_fromUtf8("sourceTextEdit"))
            self.gridLayout.addWidget(self.sourceTextEdit, 0, 0, 1, 3)
            self.sourceLangComboBox = QtGui.QComboBox(FosayForm)
            self.sourceLangComboBox.setObjectName(_fromUtf8("sourceLangComboBox"))
            self.sourceLangComboBox.addItems(sorted([key for key in long_names.values()]))
            self.gridLayout.addWidget(self.sourceLangComboBox, 1, 0, 1, 1)
            self.translateButton = QtGui.QPushButton(FosayForm)
            self.translateButton.setObjectName(_fromUtf8("translateButton"))
            self.gridLayout.addWidget(self.translateButton, 1, 1, 1, 1)
            self.targetLangComboBox = QtGui.QComboBox(FosayForm)
            self.targetLangComboBox.setObjectName(_fromUtf8("targetLangComboBox"))
            self.targetLangComboBox.addItems(sorted([key for key in long_names.values()]) + ["*caseframe"])
            self.gridLayout.addWidget(self.targetLangComboBox, 1, 2, 1, 1)
            self.targetTextEdit = QtGui.QTextEdit(FosayForm)
            self.targetTextEdit.setObjectName(_fromUtf8("targetTextEdit"))
            self.gridLayout.addWidget(self.targetTextEdit, 2, 0, 1, 3)

            QtCore.QObject.connect(self.translateButton, QtCore.SIGNAL('clicked()'), self.translateButtonClicked)

            self.retranslateUi(FosayForm)
            QtCore.QMetaObject.connectSlotsByName(FosayForm)

        def translateButtonClicked(self):
            srclan = langs[short_name[self.sourceLangComboBox.currentText()]]
            text = self.sourceTextEdit.toPlainText().strip()
            first = 'ip'
            if self.targetLangComboBox.currentText() == "*caseframe":
                tr = text_to_interlingua(text, first, srclan)
                s = ''
                for item in tr:
                    s += interlingua_to_str(item) + '\n' + '-'*50 + '\n'
                self.targetTextEdit.setText(s)
            else:
                trglan = langs[short_name[self.targetLangComboBox.currentText()]]
                tr = translate(text, first, srclan, [trglan])
                self.targetTextEdit.setText(friendly_output(tr[0]))

        def retranslateUi(self, FosayForm):
            FosayForm.setWindowTitle(QtGui.QApplication.translate("FosayForm", "fosay translator " + __version_info__[0] + " " + __version__, None, QtGui.QApplication.UnicodeUTF8))
            self.translateButton.setText(QtGui.QApplication.translate("FosayForm", ">>", None, QtGui.QApplication.UnicodeUTF8))


    #if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FosayForm = QtGui.QWidget()
    ui = Ui_FosayForm()
    ui.setupUi(FosayForm)
    FosayForm.show()
    sys.exit(app.exec_())
except ImportError:
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
            self.target_combo_box['values'] = [key for key in long_names.values()] + ["*caseframe"]

            #init target_text
            self.target_text = Text(self, width=80, height=10, font=11)
            self.target_text.config(state=DISABLED)
            #self.target_text.pack(anchor=S)
            self.target_text.grid(sticky="EW")

            for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

        def trans(self):
            srclan = langs[short_name[self.source_combo_box.get()]]
            text = self.source_text.get('1.0', 'end').strip()
            first = 'ip'
            self.target_text.config(state=NORMAL)
            self.target_text.delete('1.0', 'end')
            if self.target_combo_box.get() == "*caseframe":
                tr = text_to_interlingua(text, first, srclan)
                s = ''
                for item in tr:
                    s += interlingua_to_str(item) + '\n' + '-'*50 + '\n'
                self.target_text.insert('end', s)
            else:
                trglan = langs[short_name[self.target_combo_box.get()]]
                tr = translate(text, first, srclan, [trglan])
                self.target_text.insert('end', friendly_output(tr[0]))
            self.target_text.config(state=DISABLED)




    #feet_entry.focus()
    #root.bind('<Return>', calculate)
    root = Tk()
    root.title("fosay translator " + __version_info__[0] + " " + __version__)
    tf = TranslatorFrame(root)
    root.mainloop()