from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QRadioButton, QGroupBox, QPushButton, QButtonGroup, QListWidget, QTextEdit, QLineEdit, QInputDialog, QFileDialog)
from PIL import Image 
from PIL import ImageFilter
from PIL import ImageEnhance 
import os
from PyQt5.QtGui import QPixmap

class ImageProcessor():
    def __init__(self):
        self.picture = None
        self.filename = None
        self.folder = 'Modified/'

    def loadImage(self, filename):
        self.filename = filename
        picture_path = os.path.join(workdir, filename)
        self.picture = Image.open(picture_path)


    def showImage(self, path):
        inscription1.hide()
        pixmap = QPixmap(path)
        w, h = inscription1.width(), inscription1.height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        inscription1.setPixmap(pixmap)
        inscription1.show()
    
    def do_bw(self):
        self.picture = self.picture.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.folder, self.filename)
        self.showImage(image_path)
    
    def saveImage(self):
        path = os.path.join(workdir, self.folder)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.picture.save(image_path)

    def do_flip(self):
        self.picture = self.picture.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.folder, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.picture = self.picture.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.folder, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.picture = self.picture.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.folder, self.filename)
        self.showImage(image_path)

    def pic_contrast(self):
        self.picture = ImageEnhance.Contrast(self.picture)
        self.picture = self.picture.enhance(1.5)
        self.saveImage()
        image_path = os.path.join(workdir, self.folder, self.filename)
        self.showImage(image_path)
def showChosenImage():
    if widget1.currentRow() >= 0:
        filename = widget1.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

def chooseWorkdir():
    global workdir
    while True:
        try:
            workdir = QFileDialog.getExistingDirectory()
            break
        except:
            inf = QMessageBox()
            inf.setText('Не выбрана папка с картинками')
            inf.exec_()


def filter(files, extensions):
    result = list()
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result


def showFilenameSList():
    chooseWorkdir()
    extensions = ['.jpg', '.png', '.bmp', '.jpeg', '.gif']
    try:
        load = filter(os.listdir(workdir), extensions)
    except:
        inf = QMessageBox()
        inf.setText('Не выбрана папка с картинками')
        inf.exec_()
    widget1.clear()
    try:
        widget1.addItems(load)
    except:
        chooseWorkdir()


app = QApplication([])
main_win = QWidget()

workdir = ''
'''files = os.listdir(workdir)
print(files)'''

workimage = ImageProcessor()
inscription1 = QLabel('Картинка')
widget1 = QListWidget()
button1 = QPushButton('Папка')
button2 = QPushButton('Лево')
button3 = QPushButton('Право')
button4 = QPushButton('Зеркало')
button5 = QPushButton('Резкость')
button6 = QPushButton('Ч/б')


layout1 = QVBoxLayout()
layout3 = QVBoxLayout()
countur2 = QHBoxLayout()
countur4 = QHBoxLayout()

layout1.addWidget(button1)
layout1.addWidget(widget1)
layout3.addWidget(inscription1)
countur2.addWidget(button2)
countur2.addWidget(button3)
countur2.addWidget(button4)
countur2.addWidget(button5)
countur2.addWidget(button6)

layout3.addLayout(countur2)

countur4.addLayout(layout1, 20)
countur4.addLayout(layout3, 80)

main_win.setLayout(countur4)

button1.clicked.connect(showFilenameSList)
widget1.currentRowChanged.connect(showChosenImage)
try:
    button6.clicked.connect(workimage.do_bw)
    button4.clicked.connect(workimage.do_flip)
    button2.clicked.connect(workimage.do_left)
    button3.clicked.connect(workimage.do_right)
    button5.clicked.connect(workimage.pic_contrast)
except:
    down = QMessageBox()
    down.setText('Загрузите сначала файлы')
    down.exec_()
main_win.show()
app.exec_()











