import re
import serial
import random
import matplotlib.pyplot as plt

# Serial Start
reader = serial.Serial('/dev/ttyACM0', 9600)
print('> Start Arduino Reader')

# Data Plot
x = []
y = []
cx = 0
limx = 100
# Plot Heart Beat
plt.ion()
axes = plt.gca()
axes.set_ylim(0, 200)
line, = axes.plot(x, y, 'r-')
plt.show()

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
    if op != 'save' and op != 'heart-beat':
        val = get_values(msg_split[1])
        print(op, val)
    elif op == 'heart-beat':
        num = get_values(msg_split[1])[0]
        num = num - random.randint(0, int(num/2)) if (cx % 7 == 0) else num;
        num = num + random.randint(0, int(num / 2)) if (cx % 11 == 0) else num;
        x.append(cx)
        y.append(num)
        cx += 1
        line.set_ydata(y)
        line.set_xdata(x)
        xmin = max(0, (cx - limx))
        axes.set_xlim(xmin, xmin + (limx + 1))
        plt.draw()
        plt.pause(0.1)
    else:
        print('> save')
        get_save(reader)
