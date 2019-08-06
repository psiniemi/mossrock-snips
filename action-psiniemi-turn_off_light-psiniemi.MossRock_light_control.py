#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import mossrock as mr

CONFIG_INI = "config.ini"

def subscribe_intent_callback(hermes, intentMessage):
    conf = mr.read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)

def action_wrapper(hermes, intentMessage, conf):
    resp_msg = mr.send_off_command(mr.get_light_name(intentMessage))
    hermes.publish_end_session(intentMessage.session_id, resp_msg)

if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("psiniemi:turn_off_light", subscribe_intent_callback) \
         .start()
