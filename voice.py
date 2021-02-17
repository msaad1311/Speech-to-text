import speech_recognition as sr
import time

r=sr.Recognizer()
with sr.Microphone() as source:
    while True:
        print("Listening!")
        stime = time.time()
        audio=r.listen(source,phrase_time_limit=5)
        print(time.time()-stime)
        try:
            print('into the try method')
            s_name=r.recognize_google(audio)
            print(s_name)
        except:
            print("Error!")