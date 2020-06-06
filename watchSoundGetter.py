import pyaudio
import numpy as np
import os
import wave

class WatchSoundGetter():

    def __init__(self,CHUNK = 1024,RATE = 44100,secRec = 5):
        self.CHUNK = CHUNK
        self.RATE = RATE
        self.paudio = pyaudio.PyAudio()
        self.secRec = secRec

    def openSoundStream(self):
        self.stream = self.paudio.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,
                      frames_per_buffer=self.CHUNK)

    def record(self,name):
        frames = []
        for i in range(int(self.secRec*self.RATE/self.CHUNK)):
            data = np.fromstring(self.stream.read(self.CHUNK,exception_on_overflow = False),dtype=np.int16)
            frames.extend(data)

        self.exportWAV(frames,name)


    def closeSoundStream(self):
        self.stream.stop_stream()
        self.stream.close()

    def __del__(self):
        self.paudio.terminate()

    def exportWAV(self,frames,name):
        wf = wave.open(name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.paudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def setRecTime(self,time):
        self.secRec = int(time)

if __name__ == '__main__':
    w = WatchSoundGetter()
    w.openSoundStream()
    w.record('data.wav')
