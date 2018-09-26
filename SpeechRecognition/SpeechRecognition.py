import speech_recognition as sr

# pip install SpeechRecognition pyaudio

class BotSR(object):

    def __init__(self):
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

    def capture(self):
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
        return audio

    def speech_to_text(self, audio):
        return self.r.recognize_google(audio)










##botsr = BotSR()
##audio = botsr.capture()
##
##print(botsr.speech_to_text(audio))
