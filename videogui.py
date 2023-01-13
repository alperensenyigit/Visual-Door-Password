import sys
import cv2
import time
import numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QRect
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.FaceDetectionModule import FaceDetector
from HandTrackingModule import handDetector
from LandMarks import LandMarksFace
import webbrowser

#class for capture video from web cam
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        LandMarks = LandMarksFace()
        Hand = handDetector(detectionCon=0.75)
        detector = FaceMeshDetector(maxFaces=1)
        faceDetect = FaceDetector(minDetectionCon=0.75)
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            
            cv_img, faces = detector.findFaceMesh(cv_img, draw=False)
            cv_img, head = faceDetect.findFaces(cv_img, draw=True)
            cv_img = Hand.findHands(cv_img, draw=True )
            lmList=Hand.findPosition(cv_img,draw=False)
            
            if head:
                size = list(head[0]["bbox"])
                process = size[3]
                LandMarks.calculateFinger(cv_img,lmList)
                if process > 150:  # process is distance = 150 is approximately 50 cm, 250 -> 15 cm
                    if faces:
                        LandMarks.calculateEye(cv_img, faces, detector)
                        LandMarks.calculateMouth(cv_img, faces, detector)
                        LandMarks.calculateEyebrow(cv_img,faces,detector)
            
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

#class for display
class App(QWidget):
    #constructor for App class
    def __init__(self):
        super().__init__()

        #settings for mainwindow
        self.setWindowTitle("Mimic Door")
        self.setFixedWidth(960)
        self.setFixedHeight(500)
        self.setStyleSheet("background-color: grey;")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

        ##for screenshot
        _translate = QtCore.QCoreApplication.translate
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(_translate("MainWindow", "Take picture"))
        self.pushButton.clicked.connect(self.saveScreenshot)
        self.pushButton.setGeometry(QRect(656, 351, 293, 40))

        ##for instructors
        self.pushButton1 = QtWidgets.QPushButton(self)
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.setText(_translate("MainWindow", "User Manual"))
        self.pushButton1.setGeometry(QRect(656,449, 293, 40))
        self.pushButton1.clicked.connect(self.openInstructors)
        
        ##for password change
        self.pushButton2= QtWidgets.QPushButton(self)
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.setText(_translate("MainWindow", "Change Password"))
        self.pushButton2.clicked.connect(self.takeinputs)
        self.pushButton2.setGeometry(QRect(656, 400, 293, 40))

        ##for open logs tab
        self.pushButton3 = QtWidgets.QPushButton(self)
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton3.setText(_translate("MainWindow", "Open Logs"))
        self.pushButton3.setGeometry(QRect(656, 302, 293, 40))
        self.pushButton3.clicked.connect(self.openLogs)
        
        ##First Led for open
        self._labelLedOpen = QtWidgets.QLabel(self)
        self._labelLedOpen.setGeometry(690, 20, 90, 90)
        self.movie = QMovie("icons/loadingv1.gif")
        self._labelLedOpen.setMovie(self.movie)
        self._labelLedOpen.setScaledContents(True)
        self.movie.start()

        ##access label
        self._labelacc = QtWidgets.QLabel(self)
        self._labelacc.setGeometry(QRect(656, 120, 293, 40))

        ##led indicated with password
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.checkpw)
        timer.start(1000)

        #pixmap for images
        self.labelcheck = QtWidgets.QLabel(self)
        self.labelcheck.setGeometry(QRect(816, 20, 90, 90))
        self.pixmaptrue = QPixmap("icons/confirm-icon.png")
        self.pixmapfalse = QPixmap("icons/close-red-icon.png")
    
    #method for check password on gui
    def checkpw(self):
        f = open("checkpw.txt", "r")
        file = f.readline()
        if file == "1":
            self._labelacc.setText("    Access Granted")
            self._labelacc.setStyleSheet("background-color: green")
            self.labelcheck.setPixmap(self.pixmaptrue)
            self.labelcheck.setScaledContents(True)
        elif file == "0":
            self._labelacc.setText("    Access Denied")
            self._labelacc.setStyleSheet("background-color: red")
            self.labelcheck.setPixmap(self.pixmapfalse)
            self.labelcheck.setScaledContents(True)
        else:
            self._labelacc.setText("Taking Data...")
            self._labelacc.setStyleSheet("background-color: yellow")
            
    #method for open user manual
    def openInstructors(self):
        webbrowser.open("UserManual.pdf")

    #method for open logs
    def openLogs(self):
        webbrowser.open("logs.txt")

    #method for change password inputs
    def takeinputs(self):
        i=0
        name, self.done1 = QtWidgets.QInputDialog.getText(
         self, 'Input Dialog', 'Enter new password with numbers btw 1-9(ex. 1,2,3,4):')
        
        if self.done1 == True:
            passwordFile = open("password.txt",'w')
            
            passwordFile.write(name)

    #method for screenshot
    def saveScreenshot(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.winId())
        filename = 'Snapshot '+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
        screenshot.save(filename, 'png')

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())