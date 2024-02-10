import obspython as S
from avatar import Avatar
from multiprocessing import Process

avatarImgPath = []
neutralIdx = 4
setting_obj = None
milWait = 1000
lastIndex = 4
drawWindow = False

avatar_source_name = 'avatar_image'

class ScriptClass:
    def __init__(self, prop):
        global avatarImgPath
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
        
        source = S.obs_source_create_private("image_source", avatar_source_name, settings)
        S.obs_scene_add(scene, source)

        S.obs_scene_release(scene)
        S.obs_data_release(settings)
        S.obs_source_release(source)

    def remove_source(self):
        current_scene_as_source = S.obs_frontend_get_current_scene()
        if current_scene_as_source:
            current_scene = S.obs_scene_from_source(current_scene_as_source)
            scene_item = S.obs_scene_find_source_recursive(current_scene, avatar_source_name)
            if scene_item:
                print('scene_item:',scene_item)
                S.obs_sceneitem_remove(scene_item)
        S.obs_source_release(current_scene_as_source)

    def change_img_source(self, emotionIdx):
        global avatarImgPath
        global lastIndex
        if lastIndex!=emotionIdx:
            current_scene_as_source = S.obs_frontend_get_current_scene()
            if current_scene_as_source:
                current_scene = S.obs_scene_from_source(current_scene_as_source)
                scene_item = S.obs_scene_find_source_recursive(current_scene, avatar_source_name)
                if scene_item:
                    settings = S.obs_data_create()
                    S.obs_data_set_string(settings, "file", avatarImgPath[emotionIdx])
                    S.obs_source_update(S.obs_sceneitem_get_source(scene_item), settings)
                    S.obs_data_release(settings)
                S.obs_source_release(current_scene_as_source)
            lastIndex = emotionIdx

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

def setDrawWindow(settings):
    global drawWindow
    drawWindow = S.obs_data_get_bool(settings, 'draw_frame')


script_obj = None
avatar_obj = None
keepGoing = True

class LoopClass:
    def oneLoop(self):
        global milWait
        global avatar_obj
        global script_obj
        global keepGoing
        if keepGoing:
            print('keepGoing:',keepGoing)
            emotionIdx = avatar_obj.oneLoop(lastIndex)
            print('emotionIdx:',emotionIdx)
            script_obj.change_img_source(emotionIdx)
        else:
            S.remove_current_callback()

loopObj = LoopClass()

def add_pressed(props, prop, *args):
    global avatar_obj
    global script_obj
    global drawWindow
    S.obs_properties_apply_settings(props, setting_obj)
    script_obj = ScriptClass(props)
    avatar_obj = Avatar(0, script_path(), drawWindow)
    script_obj.create_source()
    keepGoing = True
    # loopObj.oneLoop()
    S.timer_add(loopObj.oneLoop, milWait)

def remove_pressed(props, prop):
    global keepGoing
    global avatar_obj
    global script_obj
    print('remove pressed')
    keepGoing = False
    S.timer_remove(loopObj.oneLoop)
    if avatar_obj is not None:
        avatar_obj.endSetup()
    script_obj.remove_source()
    

def script_description():
    return "add avatar source"

def script_load(settings):
    print('script loaded')
    print('angry_path:',S.obs_data_get_string(settings, 'angry_path'))
    getAllImgPaths(settings)
    setMilWait(settings)
    setDrawWindow(settings)

def script_unload():
    global avatar_obj
    global script_obj
    keepGoing = False
    if avatar_obj is not None:
        avatar_obj.endSetup()
    S.timer_remove(oneLoop)
    script_obj.remove_pressed()

def script_update(settings):
    print('script updated')
    print('sad_path:',S.obs_data_get_string(settings, 'sad_path'))
    getAllImgPaths(settings)
    setMilWait(settings)
    setDrawWindow(settings)

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

    S.obs_properties_add_bool(props, 'draw_frame', "Click to Draw Camera Feed on a separate window")
    return props
