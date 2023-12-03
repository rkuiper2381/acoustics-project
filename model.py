import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


class Model:
    def __init__(self, file):
        self.sample_rate, self.data = wavfile.read(file)
        #spectrum, freqs t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))

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

    @property
    def freqs(self):
        return self.__freqs
