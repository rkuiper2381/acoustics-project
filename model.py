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
        file = self.check_metadata(file)
        self.sample_rate, self.data = wavfile.read(file)

        self.check_channels()
        self.data = self.data.flatten()  # Flatten the 2D array to 1D
        self.spectrum, self.freqs, self.bins, self.img = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))
        self.times = np.linspace(0, self.get_duration(), num=self.data.shape[0])
        self.data_in_db = self.get_data_by_frequency()
        
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
    def t(self):
        return self.__t

    @t.setter
    def t(self, value):
        self.__t = value

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
    
    @property
    def data_in_db(self):
        return self.__data_in_db

    @data_in_db.setter
    def data_in_db(self, value):
        self.__data_in_db = value

    def find_target_frequency(self, target):
        for x in self.freqs:
            if x > target:
                break
        return x

    def frequency_check(self, target):
        target_frequency = self.find_target_frequency(target)
        idx = np.where(self.freqs == target_frequency)[0][0]
        data_db = 10 * np.log10(self.spectrum[idx])
        return data_db

    def get_data_by_frequency(self): #Returns Dictionary of dB Arrays for Low, Mid, and High Frequencies 
          x = { "Low" : self.frequency_check(100),
               "Mid" : self.frequency_check(1000),
               "High" : self.frequency_check(3000)
              }
          return x

    
    def get_duration(self):
        return self.data.shape[0]/self.sample_rate

    def plot_waveform(self):
        plt.clf() #Remove/Overwrite Spectrogram from init
        plt.plot(self.times, self.data)
        plt.title("Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.show()

    def plot_freqs(self):
        plt.figure(2)
        plt.plot(self.t, self.data_in_db["Low"])
        plt.title("Reverb Low Frequency")
        plt.xlabel("Time (s)")
        plt.ylabel("Power (dB)")
        plt.show()
        
        plt.figure(3)
        plt.plot(self.t, self.data_in_db["Mid"])
        plt.title("Reverb Mid Frequency")
        plt.xlabel("Time (s)")
        plt.ylabel("Power (dB)")
        plt.show()

        plt.figure(4)
        plt.plot(self.t, self.data_in_db["High"])
        plt.title("Reverb High Frequency")
        plt.xlabel("Time (s)")
        plt.ylabel("Power (dB)")
        plt.show()

    #Below checks for metadata, and if it finds any then creates a new wav file without the metadata and returns it, otherwise returns the file unedited
    def check_metadata(self, file):
        sound = AudioSegment.from_file(file)

        # Check if INFO metadata is present
        if b'INFO' in sound.raw_data:
            print("INFO metadata found:")
            print(sound.raw_data[b'INFO'])
            new_sound = AudioSegment(
                sound.raw_data[:sound.raw_data.find(b'INFO')],
                frame_rate=sound.frame_rate,
                sample_width=sound.sample_width,
                channels=sound.channels
            )
            new_file = file.split('.')[0]
            new_file = 'nometa' + new_file + '.wav'
            new_sound.export(new_file, format='wav')
            print(f"Metadata removed. New file saved as {new_file}")
            return new_file
        else:
            print("No INFO metadata found.")
            return file

    def check_channels(self):
        # Check if multiple channels exist, and if so convert to one channel whose data is the average of the other channels combined
        if len(self.data.shape) > 1 and self.data.shape[1] > 1:
            print("Multiple channels found. Converting to single channel.")
            self.data = np.mean(self.data, axis=1)

