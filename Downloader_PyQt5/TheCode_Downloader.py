# PyQt5 import
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

import os
from os import path
import sys
import pafy
import humanize
import youtube_dl
import urllib.request


FORM_Class,_ = loadUiType(path.join(path.dirname(__file__), "TheDesign_Downloader.ui"))


class MainApp(QMainWindow, FORM_Class):

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Ui()
        self.Handel_Buttons()


    def Handel_Ui(self):
        self.setWindowTitle("Py Downloader - Ammar An")
        self.setFixedSize(611, 290)


    def Handel_Buttons(self):
        self.pushButton_2.clicked.connect(self.Download)
        self.pushButton.clicked.connect(self.Handel_Browse)
        self.pushButton_7.clicked.connect(self.Get_Youtube_Video)
        self.pushButton_4.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse_Video)
        self.pushButton_6.clicked.connect(self.Playlist_Download)
        self.pushButton_5.clicked.connect(self.Save_Browse_Video)


    def Handel_Browse(self):
        save_palce = QFileDialog.getSaveFileName(self, caption="Save As", directory=".", filter="All Files (*.*)")
        text = str(save_palce)
        name = text.split(",")[0][2:-1]
        self.lineEdit_2.setText(name)


    def Handel_Progress(self, blocknum, blocksize, totalsize):
        read = blocknum * blocksize

        if totalsize > 0:
            percent = read * 100 / totalsize
            self.progressBar.setValue(percent)
            QApplication.processEvents()       # Not Responding


    def Download(self):
        # url - Save location - Progress
        url = self.lineEdit.text()
        #save_location = self.lineEdit_2.text()      # The Code down is to improve this

        try:
            save_location = self.lineEdit_2.text()
        except Exception:
            try:
                # I should put an spare directory for the downloaded Files using os library
                inversed_link = url[::-1]
                the_number_of_the_slash_in_the_inversed_link = inversed_link.find(r"/")
                the_number_of_the_slash_in_the_link = len(url)-the_number_of_the_slash_in_the_inversed_link
                the_name_of_the_file = url[the_number_of_the_slash_in_the_link:]
                os.mkdir(f"download_file_{the_name_of_the_file}")

                # r: for egnoring escapes(\ insted of \\) and f: for using the variables in the string
                save_location = rf"{os.getcwd()}/download_file_{the_name_of_the_file}/{the_name_of_the_file}"
                save_location = save_location.replace("\\", "/")
            except Exception:
                return

        try:
            # print("\"Trying\"The save Location is:", save_location)
            urllib.request.urlretrieve(url, save_location, self.Handel_Progress)
        except Exception:
            QMessageBox.warning(self, "Download Error", "The Download Faild")
            return

        QMessageBox.information(self, "Download Completed", f"The Download Finished")       #  \n save_location is: \n {save_location}
        # print("\"Finished\"The save Location is:", save_location)
        self.progressBar.setValue(0)
        self.lineEdit_2.setText("")
        self.lineEdit.setText("")


    def Save_Browse_Video(self):
        save = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_4.setText(save)
        self.lineEdit_6.setText(save)


    def Get_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        v = pafy.new(video_link)
        # print("v.title:", v.title)
        # print("v.duration:", v.duration)
        # print("v.rating:", v.rating)
        # print("v.author:", v.author)
        # print("v.length", v.length)
        # # print("v.keywords:", v.keywords)
        # print("v.thumb:", v.thumb)
        # print("v.videoid:", v.videoid)
        # print("v.viewcount:", v.viewcount)
        st = v.videostreams
        # print(st)

        for s in st:
            size = humanize.naturalsize(s.get_filesize())
            data = f"{s.mediatype}, {s.extension}, {s.quality}, {size}"
            self.comboBox.addItem(data)


    def Download_Youtube_Video(self):
        video_link = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()
        v = pafy.new(video_link)
        st = v.videostreams
        quality = self.comboBox.currentIndex()

        Download_video = st[quality].download(filepath = save_location)
        QMessageBox.information(self, "Download Completed", "The Download Finished")       #  \n save_location is: \n {save_location}


    def Playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()
        playlist = pafy.get_playlist(playlist_url)
        videos = playlist['items']

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))


        for video in videos :
            p = video['pafy']
            best = p.getbest(preftype='mp4')
            best.download()



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()         # Infinity loop


if __name__ == '__main__':
    main()
