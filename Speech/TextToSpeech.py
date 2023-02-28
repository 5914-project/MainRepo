from bs4 import BeautifulSoup
from gtts import gTTS
import playsound
import os

def text_to_speech(html):
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()

    tts = gTTS(text=text)
    tts.save("page.mp3")

    playsound.playsound('page.mp3', True)
    os.remove("page.mp3")

def read_html_file(filename):
    with open(filename, 'r') as file:
        html_content = file.read()
    return html_content
