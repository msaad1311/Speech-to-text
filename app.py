from flask import Flask, Response,render_template
import speech_recognition as sr
import pyaudio
import io
import soundfile as sf
import pydub
import numpy as np
from scipy.io.wavfile import write

app = Flask(__name__)


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
init_rec = sr.Recognizer()

audio1 = pyaudio.PyAudio()



def genHeader(sampleRate, bitsPerSample, channels):
    print('into genHeader')
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

@app.route('/audio')
def audio():
    # start Recording
    def sound():

        CHUNK = 1024
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        stream = audio1.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index=1,
                        frames_per_buffer=CHUNK)
        print("recording...")
        #frames = []
        first_run = True
        while True:
            print('into the while')
            if first_run:
                data = wav_header + stream.read(CHUNK)
                first_run = False
            else:
                data = stream.read(CHUNK)
            print(type(data))
            write('tester.wav',16000,np.array(data,dtype=np.int16))
            with sr.AudioFile('tester.wav') as source:
                data= init_rec.record(source)
            try:
                text = init_rec.recognize_google(data)
                print(text)
                yield(text)
            except Exception as e:
                print("Exception: "+str(e))
            

    return Response(sound())

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True,port=5000)