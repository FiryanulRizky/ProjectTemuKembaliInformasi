from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QDialog
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math

from nltk.corpus import stopwords


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 80, 280, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(50, 140, 200, 111))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(290, 140, 121, 111))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(75, 260, 160, 16))
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(300, 260, 111, 16))
        self.label2.setObjectName("label2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 80, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 10, 121, 71))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionnew = QtWidgets.QAction(MainWindow)
        self.actionnew.setObjectName("actionnew")
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.menufile.addAction(self.actionnew)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionexit)
        self.menubar.addAction(self.menufile.menuAction())

        listFile = self.pushButton_2.clicked.connect(self.getFiles)
        self.pushButton.clicked.connect(self.queryClicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Boolean Berdasarkan dokumen"))
        self.label2.setText(_translate("MainWindow", "Hasil Operasi Boolean"))
        self.pushButton.setText(_translate("MainWindow", "search"))
        self.pushButton_2.setText(_translate("MainWindow", "add text file"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.actionnew.setText(_translate("MainWindow", "new"))
        self.actionexit.setText(_translate("MainWindow", "exit"))

    def __init__(self, listFile, vocab, booleanRes, activeOperator):
        self.listFile = list()
        self.boolOperator = ['AND', 'OR', 'NOT']
        # vocab = self.checkVocab(vocab, listFile)
        self.activeOperator = activeOperator

    def getFiles(self):
        fname = QFileDialog.getOpenFileNames()
        for r in range(0, len(fname)-1):
            for j in fname[r]:
                myFile = open(j).readlines()
                for m in myFile:
                    m.translate(str.maketrans('', '', string.punctuation)).lower()
                    tokens = nltk.word_tokenize(m)
                    # listFile.append(tokens)

                    # filtering stopwords -> mengubah menjadi kata dasar
                    filteredWords = list()
                    stop_words = set(stopwords.words('english'))
                    for t in tokens:
                        if t not in stop_words:
                            filteredWords.append(t)
                            # stemming -> merubah kata yang tidak penting
                            ps = PorterStemmer()
                            output = list()
                            for f in filteredWords:
                                output.append(ps.stem(f))
                            # memasukkan data yang bersih ke dalam list
                    self.listFile.append(output)
        # print(self.listFile)
        # mencetak isi tiap tiap dokumen yang sudah bersih:
        c = 1
        print("-- Daftar dokumen dan Isinya -- ")
        for s in self.listFile:
            print('Dokumen {0} : {1}'.format(c, s))
            c+=1
        print("-- --")

    def queryClicked(self):
        userInput = self.plainTextEdit.toPlainText()
        userInput = userInput.split()
        self.boolOps(userInput)

    def boolOps(self, userInput):
        for bi in userInput:
            if bi in boolOperator:
                userInput.remove(bi)
                self.activeOperator += bi
        print("-- Query yang diinputkan pengguna --")
        print(userInput)
        print("-- --")
        print("-- Operator Boolean yang dipilih --")
        print(self.activeOperator)
        print("-- --")

        for bl in userInput:
            for i in self.listFile:
                if bl not in i:
                    booleanRes.append(0)
                else:
                    booleanRes.append(1)
        print("-- Boolean gabungan Query --")
        print(booleanRes)
        print("-- --")
        #membagi list agar tiap2 elemen ada 4
        composite_list = [booleanRes[x:x + 4] for x in range(0, len(booleanRes), 4)]
        cl = 1
        # print("-- Boolean tiap Query --")
        for sl in composite_list:
            print('Kata {0} : Hasil Boolean {1}'.format(cl, sl))
            self.plainTextEdit_2.insertPlainText('Kata {0} : Hasil Boolean {1}\n'.format(cl, sl))
            cl+= 1
        # print("-- --")

        # hitung jika boolean operator adalah AND atau OR
        print("-- Hasil Operasi Boolean --")
        if self.activeOperator == 'AND':
            flag = '1'
            print("")
            for c in range(0, len(composite_list)):
                myBinary = ''
                for l in range(0, len(composite_list[c])):
                    myBinary = myBinary + str(composite_list[c][l])
                flag = bin(int(myBinary, 2) * int(flag, 2))
            print('hasil boolean : {}'.format(flag))
            self.plainTextEdit_3.insertPlainText('hasil boolean : {}'.format(flag))
            print("-- --")
            # print("-- Boolean tiap Query --")
        elif self.activeOperator == 'OR':
            flag = '0'
            for c in range(0, len(composite_list)):
                myBinary = ''
                for l in range(0, len(composite_list[c])):
                    myBinary = myBinary + str(composite_list[c][l])
                flag = bin(int(myBinary, 2) + int(flag, 2))
            print('hasil boolean : {}'.format(flag))
            self.plainTextEdit_3.insertPlainText('hasil boolean : {}'.format(flag))
            # print("-- --")


if __name__ == "__main__":
    import sys
    #menyimpan file yang dipilih
    listFile = list()
    # vocabulary -> seluruh kata unik yang ada dalam text
    vocab = list()
    booleanRes = list()
    # boolOperator
    boolOperator = ['AND', 'OR']
    activeOperator = ''
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(listFile,vocab,booleanRes,activeOperator)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

