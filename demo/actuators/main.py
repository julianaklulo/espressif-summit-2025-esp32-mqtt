from machine import Pin

from mqtt import MQTT
from neopixel import NeoPixel
from servo import Servo


# Servo
SERVO_PIN = 18
servo = Servo(SERVO_PIN)


def control_servo(direction):
    # Set angle according to direction of the joystick
    if direction == "Left":
        angle = 180
    if direction == "Right":
        angle = 0
    if direction == "Center":
        angle = 90
    servo.set_angle(angle)

    mqtt.publish(publish_topics["servo"], angle)


# LED Ring
LED_PIN = Pin(5, Pin.OUT)
LED_N = 12
np = NeoPixel(LED_PIN, LED_N)


def control_leds(distance):
    # Constrain distance to reasonable boundaries
    dist_min = 2
    dist_max = 40
    distance = max(dist_min, min(dist_max, float(distance)))

    # Map distance to number of LEDs to turn on
    turn_on = int(((dist_max - distance) * (LED_N + 1)) / (dist_max - dist_min))

    # Calculate color
    ratio = turn_on / LED_N
    red = int(255 * ratio)
    green = int(255 * (1 - ratio))

    # Change color
    np.fill((0, 0, 0))
    for i in range(turn_on):
        np[i] = (red, green, 0)
    np.write()

    mqtt.publish(publish_topics["leds"], turn_on)


# MQTT
SERVER = "0.0.0.0"
PORT = 1883
MAIN_TOPIC = "TOPIC"

subscribe_topics_callbacks = {
   f"{MAIN_TOPIC}/sensors/joystick/direction": control_servo,
   f"{MAIN_TOPIC}/sensors/distance/value": control_leds,
}

publish_topics = {
    "servo": f"{MAIN_TOPIC}/actuators/servo/angle",
    "leds": f"{MAIN_TOPIC}/actuators/leds/qty_on",
}


def message_dispatcher(topic, data):
    topic = topic.decode("utf-8")
    message = data.decode("utf-8")
    print(f"Received '{message}' on '{topic}'")

    # Dispatch message to topic callback
    callback = subscribe_topics_callbacks[topic]
    callback(message)


mqtt = MQTT(SERVER, PORT, "actuators")
mqtt.set_callback(message_dispatcher)
mqtt.connect()

for topic in subscribe_topics_callbacks.keys():
    mqtt.subscribe(topic)

mqtt.receive_messages()
