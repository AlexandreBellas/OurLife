import matplotlib.pyplot as plt
from firebase import firebase
import requests as request
import re
import serial
import random
import json
import os

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

#o dado do CPF vem do programa principal na dragon
def getCPF():
	CPF = int(input("CPF: "))

	return CPF

def get_operation(msg):
    msg_split = msg.strip().strip('\\r').split(': ')
    op = msg_split[0]
    return op, msg_split


def get_values(val):
    num = list(map(int, re.findall(r'\d+', val)))
    return num


def getData():
	msg_hbeat = reader.readline().decode().strip()
	msg_pression_systolic = reader.readline().decode().strip()
	msg_pression_diastolic = reader.readline().decode().strip()
	msg_temperature = reader.readline().decode().strip()

	result = {}    
	result['batimentos'] = msg_hbeat
	result['PAS'] = msg_pression_systolic
	result['PAD'] = msg_pression_diastolic
	result['temperatura'] = msg_temperature
    	return result


#obter todas as infos do firebase de todos os pacientes
#specific e o cpf requerido
def getFirebase(path, specific=0):
	result = fb.get(path, None)
	
	if specific == 0:
		for i, v in result.items():
			pathcpf = "/" + v
			infos = fb.get(v, None)
			for j, value in infos.items():
				print(j + ": " + value)
	else:
		for i, v in result.items():
			if v == specific:
				break;

		specific = "/" + str(specific)
		result = fb.get(specific, None)
		for i, v in result.items():
			print(i + ": " + v)

#jogar no firebase
def postFirebase(json, path):
	result = fb.post(path, json)
	print(result)

def verifyRepetition(key, path):
	result = fb.get(path, None)

	for i, v in result.items():
		if v == key:
			return False

	return True

#recebe os dados e os destina para seus lugares
def dataTreatment(CPF, placeCPF):
	#interface arduino
	data = getData()
	#transforma em json
	json_data = json.dumps(data)
	json_cpf = json.dumps(CPF)
	print(json_data)
	#print(json_cpf)

	#gambiarra para pasta de um paciente
	path = "/" + str(CPF)

	#joga no firebase
	postFirebase(json_data, path)
	if verifyRepetition(CPF, placeCPF):
		postFirebase(json_cpf, placeCPF)
	else:
		print("Esse CPF ja esta cadastrado.")

	return data

# calcula score baseado nos dados recebidos
def calculateScore(scoreRange, result):
	score = 0

	if result['batimentos'] >= 130:
		score += 3
		scoreRange[1] = 3
	elif result['batimentos'] < 40 or result['batimentos'] >= 110:
		score += 2
		scoreRange[1] = 2
	elif result['batimentos'] <= 50 or result['batimentos'] >= 100:
		score += 1
		scoreRange[1] = 1

	if result['PAS'] < 70 or result['PAS'] > 159:
		score += 3
		scoreRange[2] = 3
	elif result['PAS'] < 80 or result['PAS'] > 149:
		score += 2
		scoreRange[2] = 2
	elif result['PAS'] < 90 or result['PAS'] > 139:
		score += 1
		scoreRange[2] = 1

	if result['PAD'] >= 110:
		score += 3
		scoreRange[3] = 3
	elif result['PAD'] >= 100 or result['PAD'] <= 45:
		score += 2
		scoreRange[3] = 2
	elif result['PAD'] >= 90:
		score += 1
		scoreRange[3] = 1

	if result['temperatura'] > 39:
		score += 3
		scoreRange[0] = 3
	elif result['temperatura'] >= 38:
		score += 1
		scoreRange[0] = 1
	elif result['temperatura'] < 35:
		score += 2
		scoreRange[0] = 2		

	return score

fb = firebase.FirebaseApplication('https://babysanca-4f129.firebaseio.com', None)
place = '/info'
device = '/dev/ttyUSB0'
data = {}

CPF = 12345678910
while True:
	msg = reader.readline().decode()
	op, msg_split = get_operation(msg)
	if op != 'save' and op != 'heart-beat':
		val = get_values(msg_split[1])
		#print(op, val)
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
        	print('> Save')
		data = dataTreatment(CPF, place)
		#getFirebase(place)

		scoreRange = [0, 0, 0, 0] # 1-amarelo, 2-laranja, 3-vermelho / ordem: [temperatura, batimentos, PAS, PAD]
		score = calculateScore(scoreRange, data)
		print("O score foi " + str(score) + ".")

