from flask import Flask, request, render_template
from SpeechToText import speech_to_text
import elastic as es

app = Flask(__name__)
es.initialize()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # result = speech_to_text()
        # recipes = es.search(' '.join(result))
        recipes = es.search('green onion pepper')
        print(recipes)
        return render_template("list.html", items=recipes)
    return render_template("webpage.html")

if __name__ == '__main__':
    app.run(debug=True)