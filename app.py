from flask import Flask, request, render_template, jsonify
from SpeechToText import speech_to_text
import Barcode.BarcodeScanner as BS

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        result = speech_to_text()
        return render_template("list.html", items=result)
    return render_template("webpage.html")

@app.route('/scan-barcode', methods=['POST'])
def scan_barcode():
    image_binary = request.files['image'].read()

    # pass the image binary data to the BarcodeScanner function
    barcode = BS.BarcodeScanner(image_binary)

    return barcode

if __name__ == '__main__':
    app.run(debug=True)