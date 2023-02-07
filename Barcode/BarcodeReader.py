import requests

def BarcodeReaderFunc(bar_code):
	url = "https://barcode-lookup.p.rapidapi.com/v3/products"

	querystring = {"barcode":bar_code}

	headers = {
		"X-RapidAPI-Key": "6b4be5824amsh7b81ea3903caa37p15d0c0jsn869ea6c67723",
		"X-RapidAPI-Host": "barcode-lookup.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	data = response.json()
	titles = []
	titles.append(data['products'][0]['title'])
	return titles