import serial
import requests
from json import dumps
from datetime import datetime
reader = serial.Serial('COM3', 9600)
while True:
	value = reader.readline()
	print(value)