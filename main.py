import obspython as scene
from avatar import avatar
import multiprocessing

imgFiles = ['','','','','','','']
camIdx = 0

class scriptClass:
    def __init__(self):
        self.avatarObj = avatar(camIdx)

    def crete_source(self, camIdx):
        self.avatarObj = avatar(camIdx)



        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)
        settings = S.obs_data_create()

        self.imgIdx=0
        S.obs_data_set_string(
            settings, "file", imgFiles[self.imgIdx]
        )
        #source = S.obs_source_create_private("text_gdiplus", "test_py", settings)
        source = S.obs_source_create_private("image_source", "image_source", settings)
        S.obs_scene_add(scene, source)

        S.obs_scene_release(scene)
        S.obs_data_release(settings)
        S.obs_source_release(source)
        self.cam = cv2.VideoCapture(0)
        cv2.namedWindow("camFeed",cv2.WINDOW_AUTOSIZE)
        ret, self.frame = self.cam.read()
        cv2.imshow('camFeed', self.frame)
        cv2.waitKey(1)

    def move_text_source(self):
        current_scene_as_source = S.obs_frontend_get_current_scene()
        if current_scene_as_source:
            current_scene = S.obs_scene_from_source(current_scene_as_source)
            scene_item = S.obs_scene_find_source_recursive(current_scene, "image_source")
            if scene_item:
                settings = S.obs_data_create()
                self.imgIdx+=1
                self.imgIdx = self.imgIdx%len(imgFiles)
                S.obs_data_set_string(settings, "file", imgFiles[self.imgIdx])
                S.obs_source_update(S.obs_sceneitem_get_source(scene_item), settings)
                S.obs_data_release(settings)
            S.obs_source_release(current_scene_as_source)
        ret, self.frame = self.cam.read()
        cv2.imshow('camFeed', self.frame)
        cv2.waitKey(1)
    
    def closeCam(self):
        if self.cam is not None:
            self.cam.release()
        cv2.destroyAllWindows()
        print('closeCam called')

eg = Example()  # class created ,obs part starts

def add_pressed(props, prop):
    eg.crete_text_source()


def move_pressed(props, prop):
    eg.move_text_source()

def script_description():
    return "add text source to current scene"

def script_load(settings):
    print('script loaded')

def script_unload():
    eg.closeCam()

def script_properties():  # ui
    props = S.obs_properties_create()
    S.obs_properties_add_button(props, "button", "Add text source", add_pressed)
    S.obs_properties_add_button(
        props, "button2", "Move source +10 pixels", move_pressed
    )
    #S.obs_properties_add_string(props, "cam")

    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    S.obs_properties_add_path(props, "Avatar Angry Image Path", "File Path to the image file to display when the script detects an Angry Face", S.OBS_PATH_FILE, None)
    S.obs_properties_add_path(props, "Avatar Disgusted Image Path", "File Path to the image file to display when the script detects a Discusted Face", S.OBS_PATH_FILE, None)
    S.obs_properties_add_path(props, "Avatar Fearful Image Path", "File Path to the image file to display when the script detects a Fearful Face", S.OBS_PATH_FILE, None)
    S.obs_properties_add_path(props, "Avatar Happy Image Path", "File Path to the image file to display when the script detects a Happy Face", S.OBS_PATH_FILE, None)
    S.obs_properties_add_path(props, "Avatar Neutral Image Path", "File Path to the image file to display when the script detects a Neutral Face", S.OBS_PATH_FILE, None)
    S.obs_properties_add_path(props, "Avatar Sad Image Path", "File Path to the image file to display when the script detects a Sad Face", S.OBS_PATH_FILE, None)
    S.obs_properties_add_path(props, "Avatar Surprised Image Path", "File Path to the image file to display when the script detects a Surprised Face", S.OBS_PATH_FILE, None)
    
    return props
