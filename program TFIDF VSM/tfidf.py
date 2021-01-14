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
        self.plainTextEdit_2.setGeometry(QtCore.QRect(50, 140, 131, 111))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(190, 140, 121, 111))
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.plainTextEdit_4 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(320, 140, 131, 111))
        self.plainTextEdit_4.setObjectName("plainTextEdit_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 260, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 260, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(370, 260, 60, 16))
        self.label_3.setObjectName("label_3")
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
        self.label.setText(_translate("MainWindow", "boolean operator"))
        self.label_2.setText(_translate("MainWindow", "tf-idf"))
        self.label_3.setText(_translate("MainWindow", "vsm"))
        self.pushButton.setText(_translate("MainWindow", "search"))
        self.pushButton_2.setText(_translate("MainWindow", "add text file"))
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.actionnew.setText(_translate("MainWindow", "new"))
        self.actionexit.setText(_translate("MainWindow", "exit"))

    def __init__(self, listFile, vocab, hasilTF, documentFreq, tfidf, finalTfidf, rankTfidf, booleanRes,
                 activeOperator):
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
        for s in self.listFile:
            print('Dokumen {0} : {1}'.format(c, s))
            c+=1

    def queryClicked(self):
        userInput = self.plainTextEdit.toPlainText()
        userInput = userInput.split()
        self.boolOps(userInput)
        self.tfidfOps(userInput)
        self.vsmOps(userInput)

    def boolOps(self, userInput):
        for bi in userInput:
            if bi in boolOperator:
                userInput.remove(bi)
                self.activeOperator += bi
        print(userInput)
        print(self.activeOperator)

        for bl in userInput:
            for i in self.listFile:
                if bl not in i:
                    booleanRes.append(0)
                else:
                    booleanRes.append(1)
        print(booleanRes)
        # membagi list agar tiap2 elemen ada 4
        composite_list = [booleanRes[x:x + 4] for x in range(0, len(booleanRes), 4)]
        print(composite_list)

        # hitung jika boolean operator adalah AND atau OR
        if self.activeOperator == 'AND':
            flag = '1'
            for c in range(0, len(composite_list)):
                myBinary = ''
                for l in range(0, len(composite_list[c])):
                    myBinary = myBinary + str(composite_list[c][l])
                flag = bin(int(myBinary, 2) * int(flag, 2))
            print('hasil boolean : {}'.format(flag))
            self.plainTextEdit_2.insertPlainText('hasil boolean : {}'.format(flag))
        elif self.activeOperator == 'OR':
            flag = '0'
            for c in range(0, len(composite_list)):
                myBinary = ''
                for l in range(0, len(composite_list[c])):
                    myBinary = myBinary + str(composite_list[c][l])
                flag = bin(int(myBinary, 2) + int(flag, 2))
            print('hasil boolean : {}'.format(flag))
            self.plainTextEdit_2.insertPlainText('hasil boolean : {}'.format(flag))
    def tfidfOps(self, userInput):
        # menghitung TF dari nilai input
        for it in range(0, len(userInput)):
            for lf in range(0, len(self.listFile)):
                count = 0
                for j in range(0, len(self.listFile[lf])):
                    if (self.listFile[lf][j] == userInput[it]):
                        if userInput[it] == self.listFile[lf][j]:
                            count += 1
                        else:
                            count += 0
                hasilTF.append(count)

        finalTF = [hasilTF[x:x + len(self.listFile)] for x in range(0, len(hasilTF), len(self.listFile))]
        print('hasil TF : ', finalTF)

        # menghitung DF -> document frequency -> seberapa banyak dokumen yang mengandung sebuah kata
        print('document frequency :\n')
        for d in range(0, len(userInput)):
            dfCount = 0
            for e in self.listFile:
                if userInput[d] in e:
                    dfCount = dfCount + 1
                else:
                    dfCount = dfCount + 0
            documentFreq.append(dfCount)
        print('Hasil document frequency : {} '.format(documentFreq))
        # merubah IDF
        for df in range(0, len(documentFreq)):
            documentFreq[df] = math.log(4 / documentFreq[df])
        print(documentFreq)

        # menghitung nilai TF-IDF
        for i in range(0, len(documentFreq)):
            for j in range(0, len(finalTF)):
                for k in range(0, len(finalTF[j])):
                    tfidf.append(documentFreq[i] * finalTF[j][k])
        finalTfidf = [tfidf[x:x + len(self.listFile)] for x in range(0, len(tfidf), len(self.listFile))]
        print('hasil TF-IDF : \n {}'.format(finalTfidf))

        # ranking tf idf
        rankTfidf = [sum(x) for x in zip(*finalTfidf)]
        c = 0
        for r in rankTfidf:
            c += 1
            print('Dokumen {0} dengan nilai : {1}'.format(c, r))
            self.plainTextEdit_3.insertPlainText('Dokumen {0} dengan nilai : {1} \n'.format(c, r))
    def vsmOps(self, userInput):
        uniqueWords = list()
        # ['breakthrough', 'drug', 'schizophrenia', 'new', 'approach', 'treatment', 'hope', 'patient']
        q = list()
        listTF = list()
        finalTF = list()
        dfiList = list()
        idfList = list()
        bobotQ = list()
        bobotPerDokumen = list()
        docSimilarity = list()
        finalDocSimilarity = list()
        indexingTerm = list()
        querySimilarity = 0
        totalSimilaritas = list()
        kolomBobotDokumen = list()

        for i in range(0, len(self.listFile)):
            for w in self.listFile[i]:
                if w not in uniqueWords:
                    uniqueWords.append(w)
        print('Unique words : ', uniqueWords)

        # take user input
        userQuery = userInput
        # ['new', 'drug', 'treatment']

        # membuat list Q (query) untuk tf-idf
        for uni in uniqueWords:
            if uni not in userQuery:
                q.append(0)
            else:
                q.append(1)
        print('kolom Q : ', q)
        # [0, 1, 0, 1, 0, 1, 0, 0]

        # membuat list-TF
        for uni in uniqueWords:
            temp = 0
            for w in self.listFile:
                if uni in w:
                    temp = w.count(uni)
                    listTF.append(temp)
                else:
                    listTF.append(0)
        print('TF : ', listTF)

        finalTF = [listTF[x:x + len(self.listFile)] for x in range(0, len(listTF), len(self.listFile))]

        print('final tf : ', finalTF)
        # [[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1]]

        # menghitung idf -> bug tidak bisa jika ada angka 2
        for st in finalTF:
            dfiList.append(sum(st))
            #  if(finalTF[f] > 1):
            #   idfFlag+=1
            #   idfList.append(idfFlag)
            # else:
            #   idfFlag += finalTF[f]
            #   idfList.append(idfFlag)
        print('dfi list : ', dfiList)

        # menghitung idf
        for d in dfiList:
            idfTemp = 0
            idfTemp = len(self.listFile) / d
            idfTemp = math.log(idfTemp)
            idfList.append(idfTemp)
        print('Hasil IDF : ', idfList)
        # [1.3862943611198906, 0.6931471805599453, 0.0, 0.28768207245178085, 1.3862943611198906, 1.3862943611198906, 1.3862943611198906, 1.3862943611198906]

        # menghitung bobot query
        for qi in range(0, len(q)):
            bobotQ.append(q[qi] * idfList[qi])

        # menghitung bobot per dokumen:
        for to in range(0, len(finalTF)):
            for u in range(0, len(finalTF[to])):
                bobotPerDokumen.append(finalTF[to][u] * bobotQ[to])
        print('bobot per dokumen : ', bobotPerDokumen)

        # bobot per dokumen (FIX)
        finalBobotPerDokumen = [bobotPerDokumen[x:x + len(self.listFile)] for x in
                                range(0, len(bobotPerDokumen), len(self.listFile))]

        print('bobot kata per dokumen (final) : ', finalBobotPerDokumen)

        kolomBobotDokumen = [sum(x) for x in zip(*finalBobotPerDokumen)]
        print('=' * 100)
        print('jumlah bobot dokumen per kolom : ', kolomBobotDokumen)
        print('=' * 100)

        # menghitung document docSimilarity

        for a in range(0, len(finalBobotPerDokumen)):
            for b in finalBobotPerDokumen[a]:
                b = math.pow(b, 2)
                docSimilarity.append(b)

        docSimilarity = ([sum(i) for i in zip(*finalBobotPerDokumen)])

        for ds in docSimilarity:
            ds = math.sqrt(ds)
            finalDocSimilarity.append(ds)
        print('Doc similarity : ', finalDocSimilarity)

        # menghitung query similarity:
        tempQ = 0
        for a in range(0, len(bobotQ)):
            tempQ = tempQ + pow(bobotQ[a], 2)
        querySimilarity = math.sqrt(tempQ)
        print('nilai query similarity : ', querySimilarity)

        # menghapus nilai 0 pada query
        for bq in bobotQ:
            if bq == 0:
                bobotQ.remove(bq)
        print('bobot query : ', bobotQ)

        # indexing term
        for bt in range(0, len(bobotQ)):
            indexingTerm.append(bobotQ[bt] * kolomBobotDokumen[bt])
        print('index term : ', indexingTerm)

        # totalSimilaritas
        for t in range(0, len(indexingTerm)):
            totalSimilaritas.append(indexingTerm[t] / querySimilarity * docSimilarity[t])

        print(totalSimilaritas)
        totNum = 0
        for tot in totalSimilaritas:
            totNum += 1
            self.plainTextEdit_4.insertPlainText('Dokumen {} : {}\n'.format(totNum, tot))
    def wtsOps(self, userInput):
        pass

if __name__ == "__main__":
    import sys
    #menyimpan file yang dipilih
    listFile = list()
    # vocabulary -> seluruh kata unik yang ada dalam text
    vocab = list()
    # list hasil term frequencies
    hasilTF = list()
    # list document frequency
    documentFreq = list()
    # list TF-IDF
    tfidf = list()
    finalTfidf = list()
    # ranking tfidf
    rankTfidf = list()
    # boolean result
    booleanRes = list()
    # boolOperator
    boolOperator = ['AND', 'OR']
    activeOperator = ''
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(listFile,vocab,hasilTF,documentFreq,tfidf,finalTfidf,rankTfidf, booleanRes, activeOperator)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

