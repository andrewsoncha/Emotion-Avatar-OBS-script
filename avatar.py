import cv2
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
        self.lastEmotionIndex = -1
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
            emotionIdx = self.emotionDetectorObj.detect(self.lastFrame)
            if emotionIdx!=self.lastEmotionIndex:
                self.lastEmotionIndex = emotionIndex
                self.obsFunc(emotionIndex)

    def endLoop(self):
        self.continueLoop = False
        self.closeCam()