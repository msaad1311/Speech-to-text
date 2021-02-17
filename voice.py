import speech_recognition as sr
import pyaudio

while True:
    init_rec = sr.Recognizer()
    print("Let's speak!!")
    with sr.Microphone() as source:
        audio_data = init_rec.listen(source)
        print("Recognizing your text.............")
        try:
            text = init_rec.recognize_google(audio_data)
            print(text)
        except:
            print('Error while reading the file')