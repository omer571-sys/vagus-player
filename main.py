from sys import argv, exit
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import (QWidget, QApplication, QAction, QMenuBar,
    QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from time import time
from tinytag import TinyTag
from pypresence import Presence
from os import listdir

"""
Bu yazılımın tüm hakları GPLv3 lisansı altında korunmaktadır.
"""

PLAYLIST_KLASORU = ""
CLIENTID = "DISCORD RICH PRESENCE ID"

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.playlistarr = listdir(PLAYLIST_KLASORU)
        self.setFullUI()
        self.show()
        try:
            self.setRPC()
        except:
            pass
        self.openMP3File()

    def openMP3File(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist(self.player)
        for i in self.playlistarr:
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(PLAYLIST_KLASORU+"/"+i)))
        self.playlist.setCurrentIndex(0)
        self.playlist.setPlaybackMode(3)
        self.player.setPlaylist(self.playlist)
        self.player.play()
        self.buSarki = time()
        self.acik = True
        self.filename = self.playlistarr[self.playlist.currentIndex()][0:-4]
        try:
            self.updateRPC()
        except:
            pass
        self.label1.setText(self.playlistarr[self.playlist.currentIndex()])
        self.player.positionChanged.connect(self.playerValueChanged)
        self.slider.valueChanged.connect(self.sliderValueChanged)
        self.playlist.currentIndexChanged.connect(self.playlistcurrindchanged)
        tag = TinyTag.get(PLAYLIST_KLASORU+"/"+self.playlistarr[self.playlist.currentIndex()])
        self.slider.setMaximum(int(self.intToMil(tag.duration)))

    def playlistcurrindchanged(self):
        print("değişti")
        self.filename = self.playlistarr[self.playlist.currentIndex()][0:-4]
        tag = TinyTag.get(PLAYLIST_KLASORU+"/"+self.playlistarr[self.playlist.currentIndex()])
        self.label1.setText(self.filename)
        self.buSarki = time()
        self.slider.setMaximum(int(self.intToMil(tag.duration)))
        self.updateRPC()

    def setFullUI(self):
        self.setWindowTitle("Vagus Player v0.1")
        self.setMenuBars()
        self.label1 = QLabel("")
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
        self.RPC = Presence(CLIENTID)
        self.RPC.connect()

        self.RPC.update(large_image="logom", large_text="Vagus Player", state=f"Boşta", start=time()*1000)


    def updateRPC(self):
        if self.acik == True:
            self.RPC.update(large_image="logom", large_text="Vagus Player", small_image="ba_lat", small_text="Dinliyor", state=f"{self.filename} dinliyor", start=self.buSarki*1000)
        else:
            self.RPC.update(large_image="logom", large_text="Vagus Player", small_image="durdur", small_text="Durdu", state=f"{self.filename} dinliyor", start=self.buSarki*1000)

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
        """if min == min2 and sec == sec2:
            filename = 'test.mp3'
            fullpath = QDir.current().absoluteFilePath(filename)
            media = QUrl.fromLocalFile(fullpath)
            content = QMediaContent(media)
            self.player.setMedia(content)
            self.player.play()"""

    def sliderValueChanged(self):
        if self.slider.value() == self.intToMil(self.player.position()) / 1000:
            pass
        else:
            self.player.setPosition(self.slider.value())

    def durdurbaslat(self):
        if self.button1.text() == "Durdur":
            self.player.pause()
            self.button1.setText("Devam Et")
            self.acik = False
            self.updateRPC()
        else:
            self.player.play()
            self.button1.setText("Durdur")
            self.acik = True
            self.updateRPC()

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
    app = QApplication(argv)
    pencere = Window()
    exit(app.exec_())
