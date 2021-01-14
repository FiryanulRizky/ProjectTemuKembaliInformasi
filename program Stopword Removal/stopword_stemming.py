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
        MainWindow.resize(400, 260)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(50, 85, 131, 85))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(190, 85, 175, 85))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 175, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(225, 175, 111, 16))
        self.label_2.setObjectName("label_2")
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Daftar Kata StopWord"))
        self.label_2.setText(_translate("MainWindow", "Daftar Kata Stemming"))
        self.pushButton_2.setText(_translate("MainWindow", "add text file"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.actionnew.setText(_translate("MainWindow", "new"))
        self.actionexit.setText(_translate("MainWindow", "exit"))

    def __init__(self, listFile, listFile2, vocab):
        self.listFile = list()
        self.listFile2 = list()

    def getFiles(self):
        fname = QFileDialog.getOpenFileNames()
        for r in range(0, len(fname)-1):
            for j in fname[r]:
                myFile = open(j).readlines()
                for m in myFile:
                    m.translate(str.maketrans('', '', string.punctuation)).lower()
                    tokens = nltk.word_tokenize(m)

                    # filtering stopwords -> mengubah menjadi kata dasar
                    filteredWords = list()
                    filteredWords2 = list()
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

                        elif t in stop_words:
                            filteredWords2.append(t)
                            # stopWord -> menyaring kata tidak penting
                            output2 = list()
                            for f2 in filteredWords2:
                                output2.append(f2)
                            self.listFile2.append(output2)

        # mencetak StopWord pada tiap tiap dokumen:
        cs = 1
        print ("Daftar Kata StopWord")
        for s2 in self.listFile2:
            print('Dokumen {0} : {1}'.format(cs, s2))
            self.plainTextEdit_2.insertPlainText('Dokumen {0} : {1}\n'.format(cs, s2))
            cs+= 1

        # mencetak isi tiap tiap dokumen yang sudah bersih (Stemming):
        c = 1
        print ("Daftar Kata Stemming")
        for s in self.listFile:
            print('Dokumen {0} : {1}'.format(c, s))
            self.plainTextEdit_3.insertPlainText('Dokumen {0} : {1}\n'.format(c, s))
            c+=1

if __name__ == "__main__":
    import sys
    #menyimpan file yang dipilih
    listFile = list()
    listFile2 = list()
    # vocabulary -> seluruh kata unik yang ada dalam text
    vocab = list()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(listFile, listFile2, vocab)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

