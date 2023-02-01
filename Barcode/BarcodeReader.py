import requests

def BarcodeReader(bar_code):
	url = "https://product-lookup-by-upc-or-ean.p.rapidapi.com/code/" + bar_code

	headers = {
		"X-RapidAPI-Key": "3b0e8b3764mshf99db17679a58cfp1ef850jsn9dc26761051c",
		"X-RapidAPI-Host": "product-lookup-by-upc-or-ean.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers)

	#print(response.text['category'])