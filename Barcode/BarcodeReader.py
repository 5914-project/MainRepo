import requests

def BarcodeReaderFunc(bar_code):
	url = "https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/" + bar_code

	headers = {
		"X-RapidAPI-Key": '19fa1a4ab8mshe730d4186e3f720p1da58bjsnd5a11ce6c2a4',
		"X-RapidAPI-Host": "product-lookup-by-upc-or-ean.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers)

	data = response.json()
	category = data.get("product").get("category")
	return category