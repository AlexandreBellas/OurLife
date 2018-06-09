from firebase import firebase
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
	result['oximetro'] = input("Oxigenio: ")
	result['pressao'] = input("Pressao: ")
	result['temperatura'] = input("Temperatura: ")

	if result['batimentos'] != '-':
		result['batimentos'] = int(result['batimentos'])

	if result['oximetro'] != '-':
		result['oximetro'] = int(result['oximetro'])

	#Gambiarra da pressao sistolica e diastolica
	if result['pressao'] != '-':
		result['pressao'] = str(result['pressao'] + "/" + str(int(result['pressao'])-30))

	if result['temperatura'] != '-':
		result['temperatura'] = int(result['temperatura'])

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
	print(json_cpf)

	#gambiarra para pasta de um paciente
	path = "/" + str(CPF)

	#joga no firebase
	postFirebase(json_data, path)
	if verifyRepetition(CPF, placeCPF):
		postFirebase(json_cpf, placeCPF)
	else:
		print("Esse CPF ja esta cadastrado.")

fb = firebase.FirebaseApplication('https://babysanca-4f129.firebaseio.com', None)
place = '/info'

while True:
	while True:
		CPF = getCPF()
		if len(str(CPF)) != 11:
			print("Insira um CPF valido.")
		else:
			break

	dataTreatment(CPF, place)
	getFirebase(place)