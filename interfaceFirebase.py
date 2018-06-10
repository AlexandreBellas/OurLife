from firebase import firebase
import serial
import json
import request
import os

#o dado do CPF vem do programa principal na dragon
def getCPF():
	CPF = int(input("CPF: "))

	return CPF

#os dados abaixos são pegos do arduino
def getData():
	result = {}
	result['batimentos'] = input("Batimentos: ")
	result['PAS'] = input("Pressao PAS: ")
	result['PAD'] = input("Pressao PAD: ")
	result['temperatura'] = input("Temperatura: ")

	if result['batimentos'] != '-':
		result['batimentos'] = int(result['batimentos'])

	if result['PAS'] != '-':
		result['PAS'] = int(result['PAS'])

	if result['PAD'] != '-':
		result['PAD'] = int(result['PAD'])

	if result['temperatura'] != '-':
		result['temperatura'] = float(result['temperatura'])

	return result

#obter todas as infos do firebase de todos os pacientes
#specific é o cpf requerido
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
		if int(v) == key:
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
	print(json_cpf)

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

	if result['temperatura'] > 39:
		score += 3
		scoreRange[0] = 3
	elif result['temperatura'] >= 38:
		score += 1
		scoreRange[0] = 1
	elif result['temperatura'] < 35:
		score += 2
		scoreRange[0] = 2

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

	return score

fb = firebase.FirebaseApplication('https://babysanca-4f129.firebaseio.com', None)
place = '/info'
device = '/dev/ttyUSB0'
data = {}

while True:
	while True:
		CPF = getCPF()
		if len(str(CPF)) != 11:
			print("Insira um CPF valido.")
		else:
			break

	data = dataTreatment(CPF, place)
	getFirebase(place)

	scoreRange = [0, 0, 0, 0] # 1-amarelo, 2-laranja, 3-vermelho / ordem: [temperatura, batimentos, PAS, PAD]
	score = calculateScore(scoreRange, data)
	print("O score foi " + str(score) + ".")
	# score total e faixa de cada medida calculados!