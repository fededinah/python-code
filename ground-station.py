#!/usr/bin/env python3
import serial
from paho.mqtt import client as mqtt
import random
import time
import json

def HoverTest(oldJson):
	print(oldJson)

	data2 = json.loads(oldJson)
	field_key = 'throttle'
	if field_key in data2:
		data2[field_key] = 1380
	modified_json = json.dumps(data2)
	print(modified_json)

    
def sendPwm(throttle, yaw, pitch, roll, channel5):
	data = {
		"throttle": throttle,
		"yaw": yaw,
		"pitch": pitch,
		"roll": roll,
		"channel5": channel5
	}
	json_string = json.dumps(data)
	print(json_string)
	client.publish(topic, json_string)




broker = 'localhost'
port = 1883
topic = "test/int"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)

client.connect(broker ,port, 60)

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer()
print("serial ok")


sendPwm(1007, 1012, 1002, 1005, 400)
time.sleep(10)
sendPwm(1007, 1012, 1002, 1005, 1500)
time.sleep(10)
sendPwm(1380, 1012, 1002, 1005, 1500)
time.sleep(10)
sendPwm(1007, 1012, 1002, 1005, 1500)
time.sleep(30)
sendPwm(700, 1012, 1002, 1005, 1500)
time.sleep(10)
sendPwm(1007, 1012, 1002, 1005, 400)




#try:
#	while True:
#		time.sleep(0.01)
#		if ser.in_waiting > 0:
			#questa riga serve a leggere i dati in arrivo dall arduino
#			line = ser.readline().decode('utf-8').rstrip()
#			json_string = json.dumps(data)

#			client.publish(topic, json_string)
#except KeyboardInterrupt:
#	client.disconnect()
#	ser.close()


