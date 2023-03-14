import requests, os

def BarcodeReaderFunc(bar_code):
	url = os.environ('RAPIDAPI_KEY')
	# url = "https://barcode-lookup.p.rapidapi.com/v3/products"

	querystring = {"barcode":bar_code}

	headers = {
		"X-RapidAPI-Key": "acfee8b3f8msh8f6c1b8c6586398p1b9d1cjsn47b1d0cd8f34",
		"X-RapidAPI-Host": "barcode-lookup.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	data = response.json()
	titles = []
	titles.append(data['products'][0]['title'])
	return titles