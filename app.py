# https://stackoverflow.com/questions/51079338/audio-livestreaming-with-python-flask

from flask import Flask, Response,render_template
import speech_recognition as sr
import pyaudio
import io
import soundfile as sf
from pydub import AudioSegment
import numpy as np
import os
from scipy.io.wavfile import write
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = int(RATE/20)
RECORD_SECONDS = 5
init_rec = sr.Recognizer()

audio1 = pyaudio.PyAudio()


def soundplot(stream):
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    return data

@app.route('/audio')
def audio():
    # start Recording
    def sound():
        stream = audio1.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index=1,
                        frames_per_buffer=CHUNK)
        print("recording...")
        frames = []
        for i in range(0,int(RATE/CHUNK * RECORD_SECONDS)):
            if i%10==0: print(i) 
            frames.append(soundplot(stream)) 
        data= np.array(frames).reshape(-1)
        print(type(data))
        try:
            print('into the try catch of saving')
            write('tester.wav',RATE,data)
        except Exception as e:
            print("Exception while saving the file: "+str(e))
        print('starting to reuse')
        with sr.AudioFile('tester.wav') as source:
            print('into the reusable')
            data= init_rec.record(source)
            print(data)
            try:
                text = init_rec.recognize_google(data)
                print(text)
                yield(text)
            except Exception as e:
                print("Exception: "+str(e))
        os.remove('tester.wav')
        

    return Response(sound())

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True,port=5000)