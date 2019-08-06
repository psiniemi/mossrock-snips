import configparser
import http.client
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def get_light_name(intentMessage):
    if intentMessage.slots.light_name.first().value:
        return intentMessage.slots.light_name.first().value
    else:
        raise Exception("Sorry, could not catch the room name")

def get_scene_name(intentMessage):
    if intentMessage.slots.scene_name.first().value:
        scene_alias = intentMessage.slots.scene_name.first().value
        scene = scene_alias
        if scene_alias == "on":
            scene = "all_on"
        elif scene_alias == "off":
            scene = "all_off"
        return scene
    else:
        raise Exception("Sorry, could not catch the scene name")

def get_dim_level(intentMessage):
    if intentMessage.slots.dim_value.first().value:
        return int(round(intentMessage.slots.dim_value.first().value/6.25, 0))
    else:
        raise Exception("Sorry, could not catch the dim level")

def send_command(command):
    resp_msg = "Sorry, something went wrong"
    try:
        conn = http.client.HTTPConnection("192.168.86.167", 8088)
        conn.request("GET", command)
        resp = conn.getresponse()
        
        if resp.status == 200:
           resp_msg = "K"
        return resp_msg
    except Exception as e:
        if str(e).startswith("Sorry,"):
            return str(e)
        else:
            return resp_msg

def send_off_command(room_name):
    return send_command("/off/" + room_name)

def send_on_command(room_name):
    return send_command("/on/" + room_name)

def send_scene_command(scene_name):
    return send_command("/scene/" + scene_name)

def send_dim_command(room_name, dim_level):
    return send_command("/dim/" + room_name + "?" + dim_level)
