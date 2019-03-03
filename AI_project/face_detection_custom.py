import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog,QMessageBox,QMainWindow,QPushButton,QLabel
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot
import cv2

# Face & eye Recognition Cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # We load the cascade for the face.
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml') # We load the cascade for the eyes.

def detect(gray, frame): # We create a function that takes as input the image in black and white (gray) and the original image (frame), and that will return the same image with the detector rectangles. 
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3,minNeighbors=5) # We apply the detectMultiScale method from the face cascade to locate one or several faces in the image.
    
    for (x, y, w, h) in faces: # For each detected face:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) # We paint a rectangle around the face.
        roi_gray = gray[y:y+h, x:x+w] # We get the region of interest in the black and white image.
        roi_color = frame[y:y+h, x:x+w] # We get the region of interest in the colored image.
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1,minNeighbors=3) # We apply the detectMultiScale method to locate one or several eyes in the image.
        for (ex, ey, ew, eh) in eyes: # For each detected eye:
            cv2.rectangle(roi_color,(ex, ey),(ex+ew, ey+eh), (0, 255, 0), 2) # We paint a rectangle around the eyes, but inside the referential of the face.
    
    return frame # We return the image with the detector rectangles.

def startwebcam_detect():
    
    video_capture = cv2.VideoCapture(0) # We turn the webcam on.

    c=1
    while True: # We repeat infinitely (until break):
    
        _, frame = video_capture.read() # We get the last frame.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # We do some colour transformations.
    
        if c%2:
            canvas = detect(gray, frame) # We get the output of our detect function.
        c=(c+1)/10
    
        cv2.imshow('Press space to exit', canvas) # We display the outputs.
        if cv2.waitKey(1) & 0xFF == ord(' '): # If we type on the keyboard:
            break # We stop the loop.

    video_capture.release() # We turn the webcam off.
    cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'CS F407 AI Assignment 2018-2019'
		self.left = 200
		self.top = 200
		self.width = 1000
		self.height = 600
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		logo = QLabel(self)
		pixmap = QPixmap('rsz_bits.png')
		logo.setPixmap(pixmap)
		logo.move(800,10)
		logo.resize(150,150)

		self.label1 = QLabel('Face detection App',self)
		self.label1.move(100,50)
		self.label1.setStyleSheet('font: bold 26px')
		self.label1.resize(400,100)

		self.label2 = QLabel('Developed by:-',self)
		self.label2.move(100,100)
		self.label2.setStyleSheet('font: bold 20px')
		self.label2.resize(400,100)
		
		self.name1 = QLabel('Murlikrishnan Tripathi',self)
		self.name1.move(120,150)
		self.name1.setStyleSheet('font: bold 16px')
		self.name1.resize(400,100)

		self.name2 = QLabel('S.R. Tejaswi',self)
		self.name2.move(120,200)
		self.name2.setStyleSheet('font: bold 16px')
		self.name2.resize(400,100)


		self.name3 = QLabel('Manik Prabhu',self)
		self.name3.move(120,250)
		self.name3.setStyleSheet('font: bold 16px')
		self.name3.resize(400,100)

		self.name4 = QLabel('P. Manobhiram',self)
		self.name4.move(120,300)
		self.name4.setStyleSheet('font: bold 16px')
		self.name4.resize(400,100)

		self.button1=QPushButton('Launch Live detection',self)
		self.button1.resize(300,100)
		self.button1.move(500,200)
		self.button1.setStyleSheet('font: 16px')
		
		self.button2=QPushButton('Identitfy from picture',self)
		self.button2.resize(300,100)
		self.button2.move(500,350)
		self.button2.setStyleSheet('font: 16px')

		self.button1.setToolTip('Click for launching live webcam detection')
		self.button2.setToolTip('Click for face detection in images')
		
		self.button1.clicked.connect(self.on_click)
		self.button2.clicked.connect(self.selectFile)

		self.show()

	@pyqtSlot()
	def on_click(self):
		self.button1.setEnabled(False)
		startwebcam_detect()
		self.button1.setEnabled(True)

	@pyqtSlot()
	def selectFile(self):
		self.button2.setEnabled(False)
		file_path=QFileDialog.getOpenFileName()[0]
		
		#convert the test image to gray image as opencv face detector expects gray images 
		frame = cv2.imread(file_path)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		frame=detect(gray,frame)
		file_path=file_path.split('.')
		print(file_path)

		buttonReply = QMessageBox.question(self, 'Saving image', "Do you want to save the processed image?",
											QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if buttonReply == QMessageBox.Yes:
			cv2.imwrite(file_path[0]+"_processed."+file_path[1],frame)
		
		cv2.imshow("processed_image",frame)
		self.button2.setEnabled(True)


if __name__ == '__main__':
	app1 = QApplication(sys.argv)
	ex = App()
	sys.exit(app1.exec_())

