import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import playsound

url = "https://www.york.ac.uk/teaching/cws/wws/webpage1.html"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

text = soup.get_text()

tts = gTTS(text=text)
tts.save("page.mp3")

playsound.playsound('page.mp3', True)