import obspython as S
from avatar import Avatar
from multiprocessing import Process

avatarImgPath = []
neutralIdx = 4
setting_obj = None
milWait = 1000

# TODO: CHANGE IT FROM RUNNING ALL IN THE BUTTON PRESSED CALLBACK FUNCTION TO A THREAD OR A TIMER OR A TICK BASED APPROACH
# USE timer_add or script_tick

class ScriptClass:
    def __init__(self, prop):
        global avatarImgPath
        self.lastEmotionIdx = neutralIdx
        print('avatarImgPath:',avatarImgPath)

    def create_source(self):
        global avatarImgPath

        current_scene = S.obs_frontend_get_current_scene()
        scene = S.obs_scene_from_source(current_scene)
        settings = S.obs_data_create()
        
        print('setting file path:',avatarImgPath[neutralIdx])

        S.obs_data_set_string(
            settings, "file", avatarImgPath[neutralIdx]
        )
        
        source = S.obs_source_create_private("image_source", "avatar_image", settings)
        S.obs_scene_add(scene, source)

        S.obs_scene_release(scene)
        S.obs_data_release(settings)
        S.obs_source_release(source)

    def change_img_source(self, emotionIdx):
        global avatarImgPath
        if self.lastEmotionIdx!=emotionIdx:
            current_scene_as_source = S.obs_frontend_get_current_scene()
            if current_scene_as_source:
                current_scene = S.obs_scene_from_source(current_scene_as_source)
                scene_item = S.obs_scene_find_source_recursive(current_scene, "avatar_image")
                if scene_item:
                    settings = S.obs_data_create()
                    S.obs_data_set_string(settings, "file", avatarImgPath[emotionIdx])
                    S.obs_source_update(S.obs_sceneitem_get_source(scene_item), settings)
                    S.obs_data_release(settings)
                S.obs_source_release(current_scene_as_source)
            self.lastEmotionIdx = emotionIdx

def getAllImgPaths(settings):
    global avatarImgPath
    print('getting all img paths')
    avatarImgPath = [
        S.obs_data_get_string(settings, 'angry_path'),
        S.obs_data_get_string(settings, 'disgusted_path'),
        S.obs_data_get_string(settings, 'fearful_path'),
        S.obs_data_get_string(settings, 'happy_path'),
        S.obs_data_get_string(settings, 'neutral_path'),
        S.obs_data_get_string(settings, 'sad_path'),
        S.obs_data_get_string(settings, 'surprised_path')
    ]
    print('avatarImgPath:',avatarImgPath)

def setMilWait(settings):
    global milWait
    fps = S.obs_data_get_int(settings, 'fps')
    milWait = int(1000/fps)
    print('milWait:',milWait)


script_obj = None
avatar_obj = None
keepGoing = True

class LoopClass:
    def oneLoop(self):
        global milWait
        global avatar_obj
        global script_obj
        global keepGoing
        print('callback called!')
        if keepGoing:
            print('keepGoing:',keepGoing)
            emotionIdx = avatar_obj.oneLoop()
            print('emotionIdx:',emotionIdx)
            script_obj.change_img_source(emotionIdx)
        else:
            S.remove_current_callback()

loopObj = LoopClass()

def add_pressed(props, prop, *args):
    global avatar_obj
    global script_obj
    S.obs_properties_apply_settings(props, setting_obj)
    print('args:',args)
    print('props:',props)
    print('____________________________')
    print('prop:',prop)
    print('settings:',setting_obj)
    script_obj = ScriptClass(props)
    avatar_obj = Avatar(0, script_path())
    script_obj.create_source()
    keepGoing = True
    # loopObj.oneLoop()
    S.timer_add(loopObj.oneLoop, milWait)

def remove_pressed(props, prop):
    global keepGoing
    global avatar_obj
    keepGoing = False
    S.timer_remove(loopObj.oneLoop)
    if avatar_obj is not None:
        avatar_obj.endSetup()
    

def script_description():
    return "add avatar source"

def script_load(settings):
    print('script loaded')
    print('angry_path:',S.obs_data_get_string(settings, 'angry_path'))
    getAllImgPaths(settings)
    setMilWait(settings)

def script_unload():
    global avatar_obj
    keepGoing = False
    if avatar_obj is not None:
        avatar_obj.endSetup()
    S.timer_remove(oneLoop)

def script_update(settings):
    print('script updated')
    print('sad_path:',S.obs_data_get_string(settings, 'sad_path'))
    getAllImgPaths(settings)
    setMilWait(settings)

def script_properties():  # ui
    props = S.obs_properties_create()
    b1 = S.obs_properties_add_button(props, "button", "Add Avatar source", add_pressed)
    S.obs_property_set_modified_callback(b1, add_pressed)
    S.obs_properties_add_button(props, "button2", "Remove Avatar Source", remove_pressed)

    S.obs_properties_add_int(props, "fps", "FPS(Avatar Refresh Rate)", 1, 1000, 30)
    S.obs_properties_add_path(props, "angry_path", "Avatar Angry Image Path", S.OBS_PATH_FILE, None, '')
    S.obs_properties_add_path(props, "disgusted_path", "Avatar Disgusted Image Path", S.OBS_PATH_FILE, None,'')
    S.obs_properties_add_path(props, "fearful_path", "Avatar Fearful Image Path", S.OBS_PATH_FILE, None,'')
    S.obs_properties_add_path(props, "happy_path", "Avatar Happy Image Path", S.OBS_PATH_FILE, None,'')
    S.obs_properties_add_path(props, "neutral_path", "Avatar Neutral Image Path", S.OBS_PATH_FILE, None,'')
    S.obs_properties_add_path(props, "sad_path", "Avatar Sad Image Path", S.OBS_PATH_FILE, None,'')
    S.obs_properties_add_path(props, "surprised_path", "Avatar Surprised Image Path", S.OBS_PATH_FILE, None,'')
    S.obs_properties_apply_settings(props, setting_obj)
    return props
