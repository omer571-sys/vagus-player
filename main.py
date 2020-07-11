import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
import time
from tinytag import TinyTag
from pypresence import Presence

"""
Bu yazılımın tüm hakları GPLv3 lisansı altında korunmaktadır.
"""

CLIENTID = "DISCORD PRESENCE ID"

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setFullUI()
        self.openMP3File()
        self.setRPC()
        self.show()

    def openMP3File(self):
        fullpath, _ = QFileDialog.getOpenFileName(self,"Vagus Player MP3 Dosya Aç", "","MP3 Dosyaları (*.mp3)")
        if(fullpath == ''):
            pass
        media = QUrl.fromLocalFile(fullpath)
        content = QMediaContent(media)
        self.player = QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()
        self.player.positionChanged.connect(self.playerValueChanged)
        self.slider.valueChanged.connect(self.sliderValueChanged)
        tag = TinyTag.get(fullpath)
        self.slider.setMaximum(int(self.intToMil(tag.duration)))

    def setFullUI(self):
        self.setWindowTitle("Vagus Player v0.1")
        self.setMenuBars()
        self.label1 = QLabel("<h2>Vagus Player</h2>")
        self.label2 = QLabel("0:0:0")
        self.label1.setAlignment(Qt.AlignCenter)
        self.button1 = QPushButton("Durdur")
        self.button1.clicked.connect(self.durdurbaslat)
        self.button2 = QPushButton("<<")
        self.button2.clicked.connect(self.gerial)
        self.button3 = QPushButton(">>")
        self.button3.clicked.connect(self.ilerial)
        self.slider = QSlider(Qt.Horizontal)

        self.layout = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QHBoxLayout()
        self.layout5 = QHBoxLayout()

        self.layout2.addWidget(self.label1)
        self.layout3.addWidget(self.slider)
        self.layout4.addWidget(self.label2)
        self.layout5.addWidget(self.button2)
        self.layout5.addWidget(self.button1)
        self.layout5.addWidget(self.button3)
        self.layout.addWidget(self.menubar)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)
        self.layout.addLayout(self.layout4)
        self.layout.addLayout(self.layout5)
        self.setLayout(self.layout)

    def setMenuBars(self):
        self.mp3Ac = QAction("MP3 Dosyası Aç", self)
        self.mp3Ac.triggered.connect(self.dosyaAc)
        self.menubar = QMenuBar()
        dosyaMenu = self.menubar.addMenu("Dosya")
        dosyaMenu.addAction(self.mp3Ac)

    def dosyaAc(self):
        self.durdurbaslat()
        self.openMP3File()

    def setRPC(self):
        RPC = Presence(CLIENTID)
        RPC.connect()

        RPC.update(state=f"{self.filename} dinliyor", start=time.time()*1000)

    def milis(self, syi):
        millis = int(syi)
        seconds=(millis/1000)%60
        seconds = int(seconds)
        minutes=(millis/(1000*60))%60
        minutes = int(minutes)
        return minutes, seconds

    def intToMil(self, sayi):
        return sayi * 1000

    def playerValueChanged(self):
        min, sec = self.milis(self.player.position())
        min2, sec2 = self.milis(self.slider.maximum())
        self.label2.setText(f"{min}:{sec}/{min2}:{sec2}")
        self.slider.setValue(self.player.position())
        if min == min2 and sec == sec2:
            filename = 'test.mp3'
            fullpath = QDir.current().absoluteFilePath(filename)
            media = QUrl.fromLocalFile(fullpath)
            content = QMediaContent(media)
            self.player.setMedia(content)
            self.player.pause()
            self.player.play()

    def sliderValueChanged(self):
        if self.slider.value() == self.intToMil(self.player.position()) / 1000:
            pass
        else:
            self.player.setPosition(self.slider.value())

    def durdurbaslat(self):
        if self.button1.text() == "Durdur":
            self.player.pause()
            self.button1.setText("Devam Et")
        else:
            self.player.play()
            self.button1.setText("Durdur")

    def gerial(self):
        if self.player.position() < 5000:
            self.player.setPosition(0)
        else:
            self.player.setPosition(self.player.position()-5000)

    def ilerial(self):
        if ((self.slider.maximum()-self.player.position()) < 5000):
            self.player.setPosition(self.slider.maximum())
        else:
            self.player.setPosition(self.player.position()+5000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = Window()
    sys.exit(app.exec_())
