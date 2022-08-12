import requests.exceptions
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.chrome.options import Options
from PyQt5.QtGui import QTextCursor
from os import path
from update_check import isUpToDate, update
from pytube import Playlist
from moviepy.editor import *
import os
from mp3_tagger import MP3File
import re


try:
    if not isUpToDate(__file__, "https://github.com/leahcim0321/MusicGetter/blob/master/mgts_2.py"):

        #update(__file__, "https://raw.githubusercontent.com/username/repo/myProgram.py")
        print("hihihihi")
except requests.exceptions.ConnectionError:
    print("Coukdnt connect")

class MyFirstGUI(QMainWindow):
    def __init__(self):
        # Initializing QDialog and locking the size at a certain value
        super(MyFirstGUI, self).__init__()
        uic.loadUi("UI_for_mg0.1.ui", self)
        self.show()
        self.setMinimumSize(650, 750)
        self.pushButton_2.clicked.connect(self.search)
        self.pushButton.clicked.connect(self.download)

    def search(self):
        try:

            self.textBrowser_2.clear()
            self.listWidget.clear()
            x = 0
            url = self.lineEdit_3.text()
            pl = Playlist(self.lineEdit_3.text())
            message = QMessageBox()

            self.textBrowser.setText(f"Album: {pl.title}\nViews: {pl.views}\nVideos: {pl.length} Video(s)")
            message.setWindowTitle("Important")
            message.setText("The program will load all infos, your program will probably freeze, in that case please "
                            "be patient and wait.")
            message.exec_()
            # ----------------------------------Get Image-----------------------------------------------
            chrome_options = Options()
            chrome_options.add_argument("--headless")

            download = "Albumcover " + pl.title
            print(download)
            site = 'https://www.google.com/search?tbm=isch&q=' + download

            driver = webdriver.Chrome(options=chrome_options)

            driver.get(site)

            driver.find_element("xpath", "//span[text()='Alle akzeptieren']").click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()
            img_tags = soup.find_all("img", class_="rg_i")

            try:
                urllib.request.urlretrieve(img_tags[0]['src'],
                                           r"temporary.jpg".format(
                                               download))  # pfad, wo die bilder gespeichert werden sollen

            except Exception as e:
                pass

            document = self.textBrowser_2.document()
            cursor = QTextCursor(document)

            p1 = cursor.position()  # returns int
            cursor.insertImage('temporary.jpg')
            # ---------------------------------------------------------------------------------------------------------
            for video in pl.videos:
                x += 1
                self.listWidget.addItem(str(f"{x:02d}. {video.title}"))
        except:
            message = QMessageBox()
            message.setWindowTitle("ERROR!")
            message.setText("The link you provided, doesnt exist. If it is a private playlist, please make it public. "
                            "It could also be that you are not connected to the internet")
            message.exec_()

    def download(self):
        ipath = self.lineEdit_4.text()
        if self.lineEdit_4.text() == "":
            print("1")
            message = QMessageBox()
            message.setWindowTitle("ERROR!")
            message.setText("Please enter the path where you want the album to go. It is recommended to create a new "
                            "folder with the name of the Album and load it into there.")
            message.exec_()
        if path.exists(ipath) and self.comboBox.currentText() == "720p":
            songs = 0

            p = Playlist(self.lineEdit_3.text())  # Youtube link
            print(p)
            dest = self.lineEdit_4.text()
            print(dest)# Path for destination

            print(f"Lade nun das Album {p.title} herunter.")
            message = QMessageBox()
            message.setWindowTitle("Important")
            message.setText(
                "The program will download all videos as mp3, your program will probably freeze, in that case "
                "please "
                "be patient and wait.")
            message.exec_()
            for video in p.videos:

                songs = songs + 1
                out_file = video.streams.filter(res="720p").first().download(output_path=dest)
                print(f"Lade {video.title} herunter.")

                cstring = re.sub("[',#.!?/*<>|]", "", video.title)
                print(cstring)

                v_path = dest + "\\" + cstring + ".mp4"  # Videopath
                # print(v_path)

                os.chdir(dest)
                head, tail = os.path.split(v_path)
                base, ext = os.path.splitext(v_path)

                mp3_file = base + ".mp3"
                # print(mp3_file)
                videoClip = VideoFileClip(v_path)

                audioclip = videoClip.audio

                audioclip.write_audiofile(mp3_file)
                audioclip.close()
                videoClip.close()

                os.remove(v_path)

                base1, ext1 = os.path.splitext(mp3_file)
                head1, tail1 = os.path.split(mp3_file)

                base1 = str(f"{songs:02d}") + ". " + tail1

                os.rename(mp3_file, base1)

                # Create MP3File instance.
                mp3 = MP3File(base1)

                # Get all tags.
                tags = mp3.get_tags()

                mp3.album = p.title
                mp3.save()
            print(f"Der Download von {p.title} ist fertig")
            songs = 0

        elif path.exists(ipath) and self.comboBox.currentText() == "480p":
            songs = 0

            p = Playlist(self.lineEdit_3.text())  # Youtube link
            print(p)
            dest = self.lineEdit_4.text()
            print(dest)  # Path for destination

            print(f"Lade nun das Album {p.title} herunter.")
            message = QMessageBox()
            message.setWindowTitle("Important")
            message.setText(
                "The program will download all videos as mp3, your program will probably freeze, in that case "
                "please "
                "be patient and wait.")
            message.exec_()
            for video in p.videos:
                songs = songs + 1
                out_file = video.streams.filter(res="480p").first().download(output_path=dest)
                print(f"Lade {video.title} herunter.")

                cstring = re.sub("[',#.!?/*<>|]", "", video.title)
                print(cstring)

                v_path = dest + "\\" + cstring + ".mp4"  # Videopath
                # print(v_path)

                os.chdir(dest)
                head, tail = os.path.split(v_path)
                base, ext = os.path.splitext(v_path)

                mp3_file = base + ".mp3"
                # print(mp3_file)
                videoClip = VideoFileClip(v_path)

                audioclip = videoClip.audio

                audioclip.write_audiofile(mp3_file)
                audioclip.close()
                videoClip.close()

                os.remove(v_path)

                base1, ext1 = os.path.splitext(mp3_file)
                head1, tail1 = os.path.split(mp3_file)

                base1 = str(f"{songs:02d}") + ". " + tail1

                os.rename(mp3_file, base1)

                # Create MP3File instance.
                mp3 = MP3File(base1)

                # Get all tags.
                tags = mp3.get_tags()

                mp3.album = p.title
                mp3.save()
            print(f"Der Download von {p.title} ist fertig")
            songs = 0


        else:
            message = QMessageBox()
            message.setWindowTitle("ERROR!")
            message.setText("The path you have given does not exist or is not valid. Please try again.")
            message.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MyFirstGUI()
    sys.exit(app.exec_())
