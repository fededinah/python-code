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

    
def sendPwm(throttle, yaw, pitch, roll, channel5, last):
	data = {
		"throttle": throttle,
		"yaw": yaw,
		"pitch": pitch,
		"roll": roll,
		"channel5": channel5
	}
	json_string = json.dumps(data)
	start = time.time()
	while(time.time()-start < last):
		client.publish(topic, json_string)
		time.sleep(0.05)
	



#------------------ Logica azioni drone ------------------





def hovering():


    throttle = 1250

    #calcolo il tempo (in secondi) che ci vuole per completare l'azione
    last = 3

    showinfo(
        title='Info',
        message=f'Adesso il drone deve sollevarsi di 1,5 metri in circa 3 secondi. Premi OK per procedere'
    )

    time.sleep(10)

    #invio i valori per farlo decollare
    sendPwm(throttle, 1012, 1005, 1002, 1500, last)


    #infine invio il json per fare stazionare il drone
    sendPwm(1007, 1012, 1005, 1002, 1500, 0.5)

    showinfo(
        title='Info',
        message=f'Adesso il drone deve essersi stazionato'
    )

    return



def forward_back(forward):

    last = 2

    if forward:

        pitch = 1100
        #invio i valori per farlo andare a dritto

        showinfo(
            title='Info',
            message=f'Adesso il drone deve andare avanti di 1 metro e impiegherà circa 2 secondi. Premi OK per procedere'
        )
        time.sleep(10)
        sendPwm(1007, 1012, pitch, 1002, 1500, last)
    else: 
        #secondo dei criteri devo selezionare il valore di pitch in questo caso coerente con la velocità e direzione selezionate
        pitch = 910

        showinfo(
            title='Info',
            message=f'Adesso il drone deve andare indietro di 1 metro e impiegherà circa 2 secondi. Premi OK per procedere'
        )
        time.sleep(10)
        #invio i valori per farlo andare indietro
        sendPwm(1007, 1012, pitch, 1002, 1500, last)

    #infine invio il json per fare stazionare il drone
    sendPwm(1007, 1012, 1005, 1002, 1500, 0.5)

    showinfo(
        title='Info',
        message=f'Adesso il drone deve essersi stazionato'
    )

    return 



def right_left(right):
    
    last = 2

    time.sleep(10)

    if right:
        #secondo dei criteri devo selezionare il valore di roll in questo caso coerente con la velocità e direzione selezionate
        roll = 1100

        showinfo(
            title='Info',
            message=f'Adesso il drone deve andare a destra di 1 metro e impiegherà circa 2 secondi. Premi OK per procedere'
        )
        time.sleep(10)
        #invio i valori per farlo andare a destra
        sendPwm(1007, 1012, 1005, roll, 1500, last)
    else: 
        #secondo dei criteri devo selezionare il valore di roll in questo caso coerente con la velocità e direzione selezionate
        roll = 904

        showinfo(
            title='Info',
            message=f'Adesso il drone deve andare a sinistra di 1 metro e impiegherà circa 2 secondi. Premi OK per procedere'
        )
        time.sleep(10)
        #invio i valori per farlo andare sinistra
        sendPwm(1007, 1012, 1005, roll, 1500, last)

    #infine invio il json per fare stazionare il drone
    sendPwm(1007, 1012, 1005, 1002, 1500, 0.5)

    showinfo(
        title='Info',
        message=f'Adesso il drone deve essersi stazionato'
    )

    return 




def rotation(right):
    
    #speed cm/min
    #distance cm

    #qui sarà da fare un calcolo per trovare il tempo di rotazione
    last = 8

    time.sleep(10)

    if right:
        #secondo dei criteri devo selezionare il valore di yaw in questo caso coerente con la velocità e la direzione selezionate
        yaw = 1200

        showinfo(
            title='Info',
            message=f'Adesso il drone deve effettuare una rotazione completa a destra e impiegherà circa 8 secondi. Premi OK per procedere'
        )
        time.sleep(10)
        #invio i valori per farlo andare a destra
        sendPwm(1007, yaw, 1005, 1002, 1500, last)
    else: 
        #secondo dei criteri devo selezionare il valore di yaw in questo caso coerente con la velocità e la direzione selezionate
        yaw = 824

        showinfo(
            title='Info',
            message=f'Adesso il drone deve effettuare una rotazione completa a sinistra e impiegherà circa 8 secondi. Premi OK per procedere'
        )
        time.sleep(10)
        #invio i valori per farlo andare sinistra
        sendPwm(1007, yaw, 1005, 1002, 1500, last)

    #infine invio il json per fare stazionare il drone
    sendPwm(1007, 1012, 1005, 1002, 1500, 0.5)

    showinfo(
        title='Info',
        message=f'Adesso il drone deve essersi stazionato'
    )

    return 


def landing():


    throttle = 700

    #calcolo il tempo (in secondi) che ci vuole per completare l'azione
    last = 5

    showinfo(
        title='Info',
        message=f'Adesso il drone deve effettuare un atterraggio e impiegherà circa 5 secondi. Premi OK per procedere'
    )

    time.sleep(10)

    #invio i valori per farlo atterrare
    sendPwm(throttle, 1012, 1005, 1002, 1500, last)

    #infine invio il json per fare stazionare il drone
    sendPwm(1007, 1012, 1005, 1002, 400, 0.5)

    showinfo(
        title='Info',
        message=f'Adesso il drone deve essersi stazionato e disarmato'
    )

    return








#------------------ Connessione -----------------------





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





#------------------ Interfaccia grafica -----------------------

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


#creo un'istanza di tk, che sarebbe una finestra
root = tk.Tk()
#definisco il titolo della finestra
root.title('Droni moves')

#definisco la grandezza e posizione della finestra e poi la centro
#widthxheight±x±y dove x è la distanza dal bordo laterale e y superiore/inferiore
window_width = 400
window_height = 250

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


action = tk.StringVar()


def do_clicked():
    match action.get():
        case "hovering":
            hovering()

        case "forward":
            forward_back(True)

        case "back":
            forward_back(False)
        
        case "right":
            right_left(True)

        case "left":
            right_left(False)

        case "rotation right":
            rotation(True)

        case "rotation left":
            rotation(False)
        
        case "landing":
            landing()


# Parameters frame
param = ttk.Frame(root)
param.pack(padx=10, pady=10, fill='x', expand=True)


# actions
combobox_label = ttk.Label(param, text="Select action:")
combobox_label.pack(fill='x', expand=True)
combobox = ttk.Combobox(param, textvariable=action)
combobox['values'] = ('hovering', 'forward', 'back', 'right', 'left', 'rotation right', 'rotation left', 'landing')
combobox['state'] = 'readonly'
combobox.pack(fill='x', expand=True)


# set parameters
do_button = ttk.Button(param, text="Do", command=do_clicked)
do_button.pack(fill='x', expand=True, pady=10)



root.mainloop()


#---------------------------------------------------------------





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


