import network
import urequests as requests
import machine
from time import sleep
import dht

TOKEN = "BBUS-8uS20MjxV9qrsQhz2AePlBZBfhpm1g" # Ubidots token
DEVICE_LABEL = "picowboard" # Device label on Ubidots
VARIABLE_LABEL_1 = "temperature"  # Label of the 1st variable
VARIABLE_LABEL_2 = "humidity"  # Lable of the 2nd variable
DELAY = 5  # Delay in seconds

# Builds the json to send the request
def build_json(variable, value):
    try:
        data = {variable: {"value": value}}
        return data
    except:
        return None

# Sending data to Ubidots Restful Webserice
def sendData(device, variable, value):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json(variable, value)

        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
            pass
    except:
        pass

# Define DHT sensor on the Pico board
sensor = dht.DHT11(machine.Pin(22))

# Your device send a random value between 0 and 100 every five second to Ubidots
while True:
    sensor.measure()	# Starts measuring
    value1 = sensor.temperature()	# Measures the temperature
    returnValue1 = sendData(DEVICE_LABEL, VARIABLE_LABEL_1, value1)	# Sends the temperature measured to Ubidots
    value2 = sensor.humidity()	# Measures the humidity
    returnValue2 = sendData(DEVICE_LABEL, VARIABLE_LABEL_2, value2)	# Sends the humidity measured to Ubidots
    sleep(DELAY)	# Rests for 5 seconds
  
