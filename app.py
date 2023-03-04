from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from Speech.SpeechToText import speech_to_text
import Barcode.BarcodeScanner as BS
import Databases.elastic as es
import Databases.user_db as users
import HelperMethods.HelperMethods as HM
from Speech.TextToSpeech import text_to_speech
import json
import items

app = Flask(__name__)
es.initialize()
db = users.initialize()

@app.route('/', methods=["GET", "POST"])
def login():
    error = None

    if request.method == 'POST':
        option = int(request.form['type'])
        username = request.form['username']
        password = request.form['password']

        if option == 1:
            if not db.find_one({'username': username}):
                db.insert_one({'username': username, 'password': password, 'ingredients':[], 'allergies':[]})
                return redirect(url_for('home'))
            else:
                error = 'Username already taken.'
        else:
            user = db.find_one({'username': username})
            if user and password == user['password']:
                return redirect(url_for('home'))
            else:
                error = 'Incorrect username or password.'
       
    return render_template('login.html', error=error)



#Home, Team, and User Feedback route
@app.route("/home/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/team/", methods=["GET", "POST"])
def team():
    return render_template("team.html")

@app.route("/feedback/", methods=["GET", "POST"])
def feedback():
    return render_template("feedback.html")


#Input Data Route
@app.route('/scan-barcode/', methods=['POST'])
def scan_barcode():
    image_binary = request.files['image'].read()

    # pass the image binary data to the BarcodeScanner function
    barcode = BS.BarcodeScanner(image_binary)
    barcode = HM.get_keyword(barcode)
    
    items.addItem(barcode)

@app.route("/speech/", methods=["GET", "POST"])
def speech():
    result = speech_to_text()
    for item in result:
        items.addItem(item)

@app.route('/text/', methods=['POST'])
def text():
    ingredients = request.json.get('ingredients')
    items.addItem(ingredients)


#Return items route
@app.route('/searchItems/', methods=['POST'])
def searchItems():
    ingredients = items.returnItems()
    return redirect(url_for('recipes', items=json.dumps(ingredients)))

#Page Reader Route
@app.route('/read-page/', methods=['POST'])
def read_page():
    webpage = request.json.get('webpage')
    text_to_speech(webpage)

@app.route('/recipes/', methods=['GET', 'POST'])
def recipes():
    items = json.loads(request.args['items'])
    esResult = es.search(items)
    return render_template('list.html', items=esResult)


if __name__ == '__main__':
    app.run(debug=True)