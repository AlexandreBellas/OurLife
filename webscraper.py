import requests
from bs4 import BeautifulSoup
import json
import re
from firebase import firebase

fb = firebase.FirebaseApplication('https://eng-soft-f1c51.firebaseio.com', None)

def getFirebase(path):
	result = fb.get(path, None)
	print(result)

def postFirebase(json, path):
	user = "admin"
	result = fb.post(path, json)
	print(result)


def load(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup

def getMoreInfo(url, data):
	soup = load(url)
	links = soup.select(".caixa-noticia-categoria")
	line = links[0].get_text()
	res = re.sub(r'\s+', ' ', line ).strip()	
	data['tags'].append(res)

def getICMC():
	url = "https://www.icmc.usp.br/eventos"
	soup = load(url)
	links = soup.select(".bloco a")
	ll = list(links)

	for l in ll:
		children = l.findChildren()
		#print(list(children))

		data = {}
		data['title'] = children[2].get_text()
		data['date'] = children[3].get_text()
		data['tags'] = ['ICMC', 'Eventos']
		data['img'] =  'https://www.icmc.usp.br' + children[0]['src']

		if l['href'][0] == '/':	# Link Interno
			data['href'] = 'https://www.icmc.usp.br' + l['href']
			getMoreInfo(data['href'], data)
		else :					# Link Externo
			data['href'] = l['href']

		json_data = json.dumps(data)
		print(json_data)
		postFirebase(json_data, '/events')

getICMC()
getFirebase('/events')

