import pyttsx3
from translate import Translator

engine = pyttsx3.init()

translator = Translator(from_lang="english", to_lang="hindi")
translation = translator.translate("Today is Tuesday")
print(translation)
engine.say("My first code on text-to-speech")
engine.say(translation)
engine.runAndWait()