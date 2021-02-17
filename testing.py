import speech_recognition as sr
from pydub import AudioSegment

sound = AudioSegment.from_mp3('tester_mp3.mp3')
sound.export('tester1.wav', format="wav")

r = sr.Recognizer()

with sr.AudioFile('tester1.wav') as source:
    audio =  r.record(source)
    
try:    
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))