from gtts import gTTS
from playsound import playsound

def convert_to_audio(text):
    my_audio = gTTS(text)
    my_audio.save('repeat.mp3')

convert_to_audio("कृपया इसे एक बार फिर से दोहराएं ?")
# playsound('single.mp3', 'return.mp3')
