from time import sleep

from joystick import Joystick
from mqtt import MQTT
from HCSR04 import HCSR04


# Joystick
JS_PIN_X = 35
JS_PIN_Y = 34
joystick = Joystick(JS_PIN_X, JS_PIN_Y)


def publish_joystick():
    direction = joystick.get_direction_x()
    mqtt.publish(publish_topics["joystick"], direction)


# Distance Sensor
US_TRIGGER = 5
US_ECHO = 18
distance_sensor = HCSR04(US_TRIGGER, US_ECHO)


def publish_distance():
    distance = distance_sensor.distance_cm()
    mqtt.publish(publish_topics["distance"], distance)


# MQTT
SERVER = "0.0.0.0"
PORT = 1883
MAIN_TOPIC = "TOPIC"

publish_topics = {
    "joystick": f"{MAIN_TOPIC}/sensors/joystick/direction",
    "distance": f"{MAIN_TOPIC}/sensors/distance/value",
}

mqtt = MQTT(SERVER, PORT, "sensors")
mqtt.connect()

while True:
    publish_joystick()
    publish_distance()

    sleep(0.5)
