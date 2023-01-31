from flask import Flask, request, render_template
from SpeechToText import speech_to_text
import elastic as es

app = Flask(__name__)
es.initialize()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        result = speech_to_text()
        es.search(' '.join(result))
        return render_template("list.html", items=result)
    return render_template("webpage.html")

if __name__ == '__main__':
    app.run(debug=True)