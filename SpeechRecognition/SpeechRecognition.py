import speech_recognition as sr
import re


# pip install SpeechRecognition pyaudio

class BotSR(object):

    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

    def capture(self):
        # record up to 5s speech
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, timeout = 5)
        return audio

    def speech_to_text(self, audio):
        return self.r.recognize_google(audio)

    def preprocess_text(self, text):
        # replace 'COMP'
        text = re.sub('(c o m p )|(comp )', 'COMP', text)

        return text

    def recognise(self):
        audio = self.capture()
        try:
            text = self.speech_to_text(audio)
            text = self.preprocess_text(text)
        except sr.UnknowValueError:
            return False

        return text








##botsr = BotSR()
##audio = botsr.capture()
##
##print(botsr.speech_to_text(audio))
