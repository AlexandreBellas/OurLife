import re
import serial
import random

# Serial Start
reader = serial.Serial('/dev/ttyACM0', 9600)
print('> Start Arduino Reader')

def get_operation(msg):
    msg_split = msg.strip().strip('\\r').split(': ')
    op = msg_split[0]
    return op, msg_split


def get_values(val):
    num = list(map(int, re.findall(r'\d+', val)))
    return num


def get_save(reader):
    msg_hbeat = reader.readline().decode().strip()
    msg_pression_systolic = reader.readline().decode().strip()
    msg_pression_diastolic = reader.readline().decode().strip()
    msg_temperature = reader.readline().decode().strip()
    val = msg_hbeat, msg_pression_systolic, msg_pression_diastolic, msg_temperature
    print(val)
    return val


while True:
    msg = reader.readline().decode()
    op, msg_split = get_operation(msg)
    if op != 'save':
        val = get_values(msg_split[1])
        print(op, val)
    else:
        print('> save')
        get_save(reader)
