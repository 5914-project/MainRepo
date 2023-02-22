from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from Speech.SpeechToText import speech_to_text
import Barcode.BarcodeScanner as BS
import ElasticSearch.elastic as es
import HelperMethods.HelperMethods as HM
from Speech.TextToSpeech import text_to_speech
import json

app = Flask(__name__)
es.initialize()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        result = speech_to_text()
        return redirect(url_for('recipes', items=json.dumps(result)))
    return render_template("webpage.html")


@app.route('/scan-barcode/', methods=['POST'])
def scan_barcode():
    image_binary = request.files['image'].read()

    # pass the image binary data to the BarcodeScanner function
    barcode = BS.BarcodeScanner(image_binary)
    barcode = HM.get_keyword(barcode)
    barcode = ['coffee']
    
    return redirect(url_for('recipes', items=json.dumps(barcode)))


@app.route('/recipes/', methods=['GET', 'POST'])
def recipes():
    items = json.loads(request.args['items'])
    esResult = es.search(items)
    return render_template('list.html', items=esResult)
    

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/read-page/', methods=['POST'])
def read_page():
    webpage = request.json.get('webpage')
    text_to_speech(webpage)

if __name__ == '__main__':
    app.run(debug=True)