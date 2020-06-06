import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
import math


REFFREQUENCY1020 = 28800
REFFREQUENCY2824 = 28800
REFFREQUENCY2500 = 25200
REFFREQUENCY1861 = 21600

class WatchSoundProcesser():
    def __init__(self):
        self.reffrequency = 28800

    def setRefFrequency(self,freq):
        self.reffrequency = freq

    def getRightData(self,data):
        return [dat[0] for dat in data]

    def getLeftData(self,data):
        return [dat[1] for dat in data]

    def importWAV(self,filename):
        samplerate, data = scipy.io.wavfile.read(filename)
        self.sampleRate = samplerate
        return [samplerate,data]

    def plotWaveForm2D(self,samplerate,data):
        length = data.shape[0] / samplerate
        time = np.linspace(0., length,len(data[:,0]))
        p = self.peakSignalDetection(data[:, 0])
        plt.plot(time, data[:, 0], label="Left channel")
        plt.legend()
        plt.plot(time[p[0]],data[p[0], 0],'x')
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    def plotWaveForm1s2D(self,samplerate,data):
        plt.plot(data[:44100, 0], label="Left channel")
        p = self.peakSignalDetection(data[:44100, 0])
        plt.legend()
        plt.plot(p[0],data[p[0], 0],'x')
        plt.xlabel("n")
        plt.ylabel("Amplitude")
        plt.show()

    def plotWaveForm1D(self,samplerate,data):
        length = len(data) / samplerate
        time = np.linspace(0., length,len(data[:]))
        p = self.peakSignalDetection(data[:])
        plt.plot(time, data[:], label="Left channel")
        plt.legend()
        plt.plot(time[p[0]],data[p[0]],'x')
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    def applyWiener(self,data):
        wData = ss.wiener(data)
        return wData

    def exportWAV(self,filename,sampleRate,data):
        scipy.io.wavfile.write(filename,sampleRate,data)

    def spectrum(self,samplerate,data):
        rightData = self.getRightData(data)
        length = len(rightData) / samplerate
        time = np.linspace(0., length, len(rightData))
        f =  np.fft.rfft(rightData*np.hanning(len(rightData)))
        freq = np.fft.fftfreq(len(rightData), d=1/samplerate)
        return [freq[0:len(f)],f]

    def peakSignalDetection(self,data1D):
        return ss.find_peaks(data1D,distance = 0.9 * 3600 * self.sampleRate/self.reffrequency)

    def getMovementFrequencyFromPeakIndex(self,sampleRate,peaks):
        fs = []
        for i in range(len(peaks[0])-1):
            delta = (peaks[0][i+1]-peaks[0][i])
            #nonAvg = 3600*sampleRate/delta
            #print(3600 *self.getDrift(self.reffrequency,nonAvg))
            fs.append(sampleRate/delta)
        return 60*60*np.mean(fs)

    def getDrift(self,refFrequency,realFrequency):
        deltaBeat = refFrequency-realFrequency
        frac = deltaBeat/refFrequency
        return frac

    def findFreqDomainPeak(self,freq,fourier):
        midIndex = np.where(freq == self.find_nearest(freq,self.reffrequency/3600))
        max = 0
        for i in range(-10,10,1):
            val = fourier[midIndex[0][0]+i]
            if val > max:
                max = val
        return np.where(fourier == max)[0][0]

    def find_nearest(self,array,value):
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
            return array[idx-1]
        else:
            return array[idx]

    def process(self,filename):
        #raw data
        dat = self.importWAV(filename)
        #self.plotWaveForm2D(dat[0],dat[1])

        #gaussian noise filtered data
        wdata = self.applyWiener(dat[1])
        self.plotWaveForm1D(dat[0],wdata)

        #spectrum analysis
        spec = self.spectrum(dat[0],dat[1])
        #plt.plot(spec[0],np.absolute(spec[1]))
        #plt.show()

        #deviation estimation from time domain data
        p = self.peakSignalDetection(self.getRightData(dat[1]))
        freqT = self.getMovementFrequencyFromPeakIndex(dat[0],p)
        H = self.getDrift(self.reffrequency,freqT)
        print('Deviation time per day for timedomain: ' + "{:5.2f}".format(H*3600) + ' s/day')

    def getBeatError(self,peaks):
        teven = []
        todd = []
        oneFramemSec = 1000/self.sampleRate
        previous = 0
        for i,pi in enumerate(peaks[0],start = 1):
            if i % 2 == 0:
                teven.append((pi-previous)*oneFramemSec)
            else:
                todd.append((pi-previous)*oneFramemSec)
            previous = pi
        return np.abs(np.median(teven)-np.median(todd))


    def analysisGUI(self,filename):
        self.sampleRate,self.frames = self.importWAV(filename)
        self.frames = self.applyWiener(self.frames)
        p = self.peakSignalDetection(self.frames[:])
        err = self.getBeatError(p)
        freqT = self.getMovementFrequencyFromPeakIndex(self.sampleRate,p)
        timeDev = self.getDrift(self.reffrequency,freqT)
        return [timeDev*3600,err]


    def plotWaveFormGUI(self):
        self.plotWaveForm1D(self.sampleRate,self.frames)


if __name__ == '__main__':
    w = WatchSoundProcesser()
    w.process('data.wav')
