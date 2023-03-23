from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from Speech.SpeechToText import speech_to_text
import Barcode.BarcodeScanner as BS
import Databases.elastic as es
import Databases.user_db as db
from Databases.User import User
import HelperMethods.HelperMethods as HM
from Speech.TextToSpeech import text_to_speech
import json, os
import Camera.CameraCapture as Camera

app = Flask(__name__)
es.initialize()
db.initialize()
USER = None

@app.route('/', methods=["GET", "POST"])
def login():
    global USER
    error = None

    if request.method == 'POST':
        option = int(request.form['type'])
        username = request.form['username']
        password = request.form['password']

        if option == 1:
            error, user = db.signup(username, password)
        else:
            error, user = db.login(username, password)
        
        if not error:
                USER = User(user)
                return redirect(url_for('home'))
       
    return render_template('login.html', error=error)



#Home, Team, and User Feedback route
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html", items={'username':USER.username})

@app.route("/team", methods=["GET", "POST"])
def team():
    return render_template("team.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    return render_template("feedback.html")


#Input Data Route
@app.route('/scan-barcode', methods=['GET', "POST"])
def scan_barcode():
    image_binary = request.files['image'].read()

    # pass the image binary data to the BarcodeScanner function
    barcode = BS.BarcodeScanner(image_binary)
    barcode = HM.get_keyword(barcode)
    
    USER.add_ingredient(barcode)
    db.update_doc(USER, USER.username)
    return USER.get_ingredients()

@app.route("/speech", methods=["GET", 'POST'])
def speech():
    result = speech_to_text()
    for item in result:
        USER.add_ingredient(item)
    
    db.update_doc(USER, USER.username)
    return USER.get_ingredients()

@app.route('/text', methods=['GET', 'POST'])
def text():
    ingredients = request.json.get('ingredients')

    USER.add_ingredient(ingredients)
    db.update_doc(USER, USER.username)
    return USER.get_ingredients()

@app.route('/savePicture', methods=['GET', 'POST'])
def savePicture():
    Camera.takePic()
    return ""

#Remove items route
@app.route('/removeItems', methods=['POST'])
def removeItems():
    USER.clear_ingredients()
    db.update_doc(USER, USER.username)
    return ""

@app.route('/removeSingleItem', methods=['POST'])
def removeSingleItem():
    item = request.json.get('itemText')
    print(item)
    USER.remove_ingredient(item)
    db.update_doc(USER, USER.username)
    return USER.get_ingredients()

#Return items route
@app.route('/searchItems', methods=['POST'])
def searchItems():
    ingredients = USER.get_ingredients()
    return redirect(url_for('recipes', items=json.dumps(ingredients)))

#Page Reader Route
@app.route('/read-page', methods=['POST'])
def read_page():
    webpage = request.json.get('webpage')
    text_to_speech(webpage)

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    items = json.loads(request.args['items'])
    esResult = es.search(items)
    return render_template('list.html', items=esResult)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))