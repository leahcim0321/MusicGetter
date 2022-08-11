from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import sys
from pytube import Playlist
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.chrome.options import Options
from PyQt5.QtGui import QTextCursor
from mgts_3 import *
import os.path
from os import path
from update_check import isUpToDate

if not isUpToDate(__file__, "https://raw.githubusercontent.com/username/repo/myProgram.py"):
   print("yady")

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
            self.lineEdit_3.setText("")
            self.textBrowser.setText(f"Album: {pl.title}\nViews: {pl.views}\nVideos: {pl.length} Video(s)")
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
            message = QMessageBox()
            message.setWindowTitle("ERROR!")
            message.setText("Please enter the path where you want the album to go. It is recommended to create a new "
                            "folder with the name of the Album and load it into there.")
            message.exec_()
        if path.exists(ipath):
            self.lineEdit_4.setText("")
        else:
            message = QMessageBox()
            message.setWindowTitle("ERROR!")
            message.setText("The path you have given does not exist or is not valid. Please try again.")
            message.exec_()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MyFirstGUI()
    sys.exit(app.exec_())
