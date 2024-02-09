import numpy as np
import argparse
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.optimizers import Adam
from keras.layers import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

class EmotionDetector:
    def __init__(self, scriptPath):
        self.model_path = scriptPath+'model.h5'
        if os.path.isfile(self.model_path):
            print(self.model_path,' is a file!')
        else:
            print(self.model_path,' is not a file!')
        self.model = self.loadModel(self.model_path)
        self.face_casc = cv2.CascadeClassifier(scriptPath+'haarcascade_frontalface_default.xml')
        cv2.ocl.setUseOpenCL(False)
        
    def loadModel(self, model_path):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(7, activation='softmax'))
        model.load_weights(model_path)
        print('EmotionDetector model loaded')
        return model
    
    def detectEmotion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_casc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
        maxindex = 4
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = self.model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
        return maxindex