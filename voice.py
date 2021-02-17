# import speech_recognition as sr
# import time

# while True:
#     r=sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening!")
#         stime = time.time()
#         audio=r.listen(source)
#         print(time.time()-stime)
#         try:
#             print('into the try method')
#             s_name=r.recognize_google(audio)
#             print(s_name)
#         except:
#             print('error')
import speech_recognition as sr
import pyaudio

while True:
    init_rec = sr.Recognizer()
    print("Let's speak!!")
    with sr.Microphone() as source:
        audio_data = init_rec.record(source, duration=1)
        # print(audio_data)
        print("Recognizing your text.............")
        text = init_rec.recognize_google(audio_data,show_all=True)
        print(text)