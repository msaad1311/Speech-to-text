import speech_recognition as sr
import time

while True:
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening!")
        stime = time.time()
        audio=r.listen(source,phrase_time_limit=1)
        print(time.time()-stime)
        try:
            print('into the try method')
            s_name=r.recognize_google(audio)
            print(s_name)
        except:
            print("Error!")