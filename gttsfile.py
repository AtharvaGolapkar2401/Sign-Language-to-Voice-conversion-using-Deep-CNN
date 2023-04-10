from gtts import gTTS
from playsound import playsound

def convert_to_audio(text):
    my_audio = gTTS(text)
    my_audio.save('ghatkopar.mp3')

convert_to_audio("via Kurla or Thane")
# playsound('single.mp3', 'return.mp3')
