import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from os import path

class Model:
    def __init__(self, file):
        if file.endswith('.mp3'):  #Converts mp3 file to wav, requires ffmpeg
            sound = AudioSegment.from_mp3(file)
            dst = file.split('.')[0]
            dst = dst + '.wav'
            sound.export(dst, format='wav')
            file = dst
            print('mp3 file converted to wav file')
        self.sample_rate, self.data = wavfile.read(file)
        self.data = self.data.flatten()  # Flatten the 2D array to 1D
        self.spectrum, self.freqs, self.bins, self.img = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))
        self.times = np.linspace(0, self.get_duration(), num=self.data.shape[0])

    @property
    def sample_rate(self):
        return self.__sample_rate

    @sample_rate.setter
    def sample_rate(self, value):
        self.__sample_rate = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def spectrum(self):
        return self.__spectrum

    @spectrum.setter
    def spectrum(self, value):
        self.__spectrum = value

    @property
    def freqs(self):
        return self.__freqs

    @freqs.setter
    def freqs(self, value):
        self.__freqs = value

    @property
    def bins(self):
        return self.__bins

    @bins.setter
    def bins(self, value):
        self.__bins = value

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, value):
        self.__img = value

    @property
    def times(self):
        return self.__times

    @times.setter
    def times(self, value):
        self.__times = value
    
    def get_duration(self):
        return self.data.shape[0]/self.sample_rate

    def plot_waveform(self):
        plt.clf() #Remove/Overwrite Spectrogram from init
        plt.plot(self.times, self.data)
        plt.show()
