'''import cv2
import multiprocessing
from emotionDetector import emotionDetector

#todo: change function call to multiprocessing signal.
# have signal be sent to obs plugin class in main.py

class avatar:
    def __init__(self, camIdx=-1):
        if camIdx!=-1:
            self.openCam(camIdx)
        else:
            self.cam = None
        self.lastFrame = None
        self.fps = 10
        self.continueLoop = True
        self.emotionIndex = -1
        self.emotionDetectorObj = emotionDetector()

    def openCam(self, camIdx):
        self.cam = cv2.videoCapture(camIdx)
    
    def closeCam(self):
        if self.cam is not None:
            self.cam.release()
        cv2.destroyAllWindows()
    
    def getNewFrame(self):
        ret, frame = self.cam.read()
        if ret:
            self.lastFrame = frame

    def mainLoop(self):
        while self.continueLoop:
            self.getNewFrame()
            self.emotionIdx = self.emotionDetectorObj.detect(self.lastFrame)

    def endLoop(self):
        self.continueLoop = False
        self.closeCam()'''

import cv2
from emotionDetector import EmotionDetector

class Avatar:
    def __init__(self, camIdx, scriptPath):
        print('avatar init!')
        self.emotionDetectorObj = EmotionDetector(scriptPath)
        self.cam = cv2.VideoCapture(camIdx)
    def oneLoop(self):
        ret, frame = self.cam.read()
        if ret:
            return self.emotionDetectorObj.detectEmotion(frame)
        else:
            return 4
        #When no image is read from cam, Neutral expression is returned
    def endSetup(self):
        cv2.destroyAllWindows()
        self.cam.release()