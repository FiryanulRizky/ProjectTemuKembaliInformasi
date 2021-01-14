from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap

import numpy as np
import math
from PIL import Image


class Ui_MainWindow(object):
    arrFromImg = 0
    maxVal = 0
    occMatrix = 0
    transMatrix = 0
    sumMatrix = 0
    normMatrix = 0
    asm = 0

    def setupUi(self, MainWindow):
        arrFromImg = 0
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 171, 161))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("programGLCM.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 20, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(190, 50, 431, 131))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Image", "GLCM"))
        self.pushButton.setText(_translate("MainWindow", "Browse Image"))
        # ketika button di click
        self.pushButton.clicked.connect(self.browseImage)
        # self.pushButton_2.setText(_translate("MainWindow", "GLCM"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "contrast"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "correlation"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "energy"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "homogeneity"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Hasil"))

    def calcContrast(self, nm):
        contrastRes = 0
        for n in range(0, len(nm)):
            for m in range(0, len(nm[n])):
                # print(nm[n][m], n, m)
                temp = nm[n][m] * math.pow((n - m), 2)
                contrastRes += temp
        print("Contrast : ", contrastRes)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(contrastRes)))

    def calcDiss(self, nm):
        dissRes = 0
        for n in range(0, len(nm)):
            for m in range(0, len(nm[n])):
                # print(nm[n][m], n, m)
                temp = nm[n][m] * abs(n - m)
                dissRes += temp
        print("Dissimilarity : ", dissRes)
        self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(str(dissRes)))

    def calcHomo(self, nm):
        homoRes = 0
        for n in range(0, len(nm)):
            for m in range(0, len(nm[n])):
                # print(nm[n][m], n, m)
                temp = nm[n][m] / (1 + math.pow((n - m), 2))
                homoRes += temp
        print("Homogeneity : ", homoRes)
        self.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(str(homoRes)))

    def caclAsm(self, nm):
        asmRes = 0
        for n in range(0, len(nm)):
            for m in range(0, len(nm[n])):
                # print(nm[n][m], n, m)
                temp = math.pow(nm[n][m], 2)
                asmRes += temp
        print("ASM : ", asmRes)
        self.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(str(asmRes)))
        return asmRes

    def caclEnergy(self, asm):
        eng = math.sqrt(asm)
        self.tableWidget.setItem(4, 0, QtWidgets.QTableWidgetItem(str(eng)))
        print("Energy : ", eng)

    def updatePixmap(self, pm, img):
        saveImg = Image.fromarray(pm)
        saveImg = saveImg.convert("RGB")
        saveImg.save("pm.jpeg")
        pixmap = QPixmap(img)
        self.label.setPixmap(QPixmap(pixmap))
        self.label.setScaledContents(True)

    def getNewMatrix(self, maxVal):
        newMat = np.zeros(shape=(maxVal + 1, maxVal + 1))
        return newMat

    def findOccurences(self, ia, nm):
        print(ia)
        for i in range(0, len(ia)):
            for j in range(0, len(ia[i]) - 1):
                findex = ia[i][j]
                sindex = ia[i][j + 1]
                # print(ia[i][j],ia[i][j+1])
                nm[int(findex)][int(sindex)] += 1
        return nm

    def normalizeMatrix(self, m):
        pass  # formula : glcmNorm = glcmVal/sum of all glcm value
        sumOfAll = np.sum(m)
        for i in range(0, len(m)):
            for j in range(0, len(m[i])):
                m[i][j] = m[i][j] / sumOfAll
        return m

    def browseImage(self):
        img, _ = QFileDialog.getOpenFileName(
            MainWindow,
            "Open image file",
            "/Users/firyan2903/Documents/imgProc",
            "Image files(*.jpg)",
        )
        loadImg = Image.open(img).resize((200, 200))
        arrFromImg = toGrayScale(loadImg)
        print(arrFromImg)

        # update pixmap
        self.updatePixmap(arrFromImg, img)

        # nilai terbesar
        # maxVal = np.amax(imgArr)
        maxVal = np.amax(arrFromImg)
        maxVal = int(maxVal)
        print(maxVal)

        # membuat matriks baru
        newMatrix = self.getNewMatrix(maxVal)
        print("Matrix baru : ", newMatrix)

        # find matrix occurences
        occMatrix = self.findOccurences(arrFromImg, newMatrix)
        print("Matrix Occurence : ", occMatrix)

        # matrix tranpose
        transMatrix = np.transpose(occMatrix)
        print("Matrix transpose : ", transMatrix)

        # sum of matrix occurences and matrix transpose
        sumMatrix = np.add(occMatrix, transMatrix)
        print("Matrix penjumlahan : ", sumMatrix)

        # matrix normalization
        normMatrix = self.normalizeMatrix(sumMatrix)
        print("Matrix normalisasi : ", normMatrix)

        # -------calculating texture------------

        # contrast
        self.calcContrast(normMatrix)
        # dissimilarity
        self.calcDiss(normMatrix)
        # homogeneity
        self.calcHomo(normMatrix)
        # asm
        asm = self.caclAsm(normMatrix)
        # energy
        self.caclEnergy(asm)


if __name__ == "__main__":
    import sys

    def toGrayScale(img):
        rgb = np.array(img)
        return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())