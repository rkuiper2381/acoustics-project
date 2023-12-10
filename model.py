import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from os import path

class Model:
    def __init__(self, file):
        if file.endswith('.mp3'):
            sound = AudioSegment.from_mp3(file)
            dst = file.split('.')[0]
            dst = dst + '.wav'
            sound.export(dst, format='wav')
            file = dst
            print('mp3 file converted to wav file')
        file = self.check_metadata(file)
        self.sample_rate, self.data = wavfile.read(file)

        self.check_channels()
        self.data = self.data.flatten()
        self.spectrum, self.freqs, self.t, self.img = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024,
                                                                      cmap=plt.get_cmap("autumn_r"))
        self.times = np.linspace(0, self.get_duration(), num=self.data.shape[0])
        self.data_in_db = self.get_data_by_frequency()
        self.rt60 = self.calc_rt60()
        print(self.get_rt60())
        self.fig, self.ax = self.create_empty_plot()  # Initialize figure and axes

    @staticmethod
    def create_empty_plot():
        fig, ax = plt.subplots()
        ax.set_title("Empty Plot")
        ax.set_xlabel("X-axis Label")
        ax.set_ylabel("Y-axis Label")
        return fig, ax
    
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

    @property
    def rt60(self):
        return self.__rt60

    @rt60.setter
    def rt60(self, value):
        self.__rt60 = value

    def find_target_frequency(self, target):
        for x in self.freqs:
            if x > target:
                break
        return x


    def frequency_check(self, target):
        target_frequency = self.find_target_frequency(target)
        idx = np.where(self.freqs == target_frequency)[0][0]
        data_db = 10 * np.log10(self.spectrum[idx])

        db_interpolated = np.interp(self.times,
                               np.linspace(0, self.get_duration(), num=len(data_db)),
                               data_db)
        return db_interpolated

    def get_data_by_frequency(self): #Returns Dictionary of dB Arrays for Low, Mid, and High Frequencies 
          data_db = { "Low" : self.frequency_check(100),
               "Mid" : self.frequency_check(1000),
               "High" : self.frequency_check(5000)
              }
          return data_db

    @staticmethod
    def first_below(array, threshold): #Finds First in array Below threshold
        for x in array:
            if x < threshold:
                break
        return x

    def calc_rt60_freq(self, freq_type="Low"):
        max_val_idx = np.argmax(self.data_in_db[freq_type])
        max_val = self.data_in_db[freq_type][max_val_idx]
        sliced_db = self.data_in_db[freq_type][max_val_idx:]

        
        max_less_5 = self.first_below(sliced_db, max_val - 5)
        max_less_5_idx = np.where(self.data_in_db[freq_type] == max_less_5)

        max_less_25 = self.first_below(sliced_db, max_val - 25)
        max_less_25_idx = np.where(self.data_in_db[freq_type] == max_less_25)

        rt20 = self.times[max_less_25_idx] - self.times[max_less_5_idx]
        rt60 = 3 * rt20

        return [rt60, max_val_idx, max_less_5_idx, max_less_25_idx]

    def calc_rt60(self):
          rt60 = { "Low" : self.calc_rt60_freq("Low"),
               "Mid" : self.calc_rt60_freq("Mid"),
               "High" : self.calc_rt60_freq("High")
              }
          return rt60

    def get_rt60(self, freq_type="Avg"):
        if freq_type not in self.data_in_db:
            if freq_type == "Avg":
                return (self.rt60["Low"][0] + self.rt60["Mid"][0] + self.rt60["High"][0]) / 3
            else:
                print(f"Invalid frequency type: {freq_type}")
                return
            
        return self.rt60[freq_type][0]
        
    def get_duration(self):
        return self.data.shape[0]/self.sample_rate

    def get_resonance(self): #Reurn Frequency of Highest Amplitude (Hz)
        idx = np.argmax(self.spectrum)//len(self.spectrum[0])
        return self.freqs[idx]

    def plot_waveform(self, ax):
        ax.clear()
        ax.plot(self.times, self.data)
        ax.set_title("Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

    #def plot_resonance(self, ax):
    #    spectrum_db = 10 * np.log10(self.spectrum)
    #    ax.clear()
    #    ax.plot(self.freqs, spectrum_db)
    #    ax.set_title("Waveform")
    #    ax.set_xlabel("Frequency (Hz)")
    #    ax.set_ylabel("Amplitude")

    def plot_rt60(self, ax, freq_type="Low"):
        if freq_type not in self.data_in_db:
            print(f"Invalid frequency type: {freq_type}")
            return

        ax.plot(self.times[self.rt60[freq_type][1]], self.data_in_db[freq_type][self.rt60[freq_type][1]], 'go')
        ax.plot(self.times[self.rt60[freq_type][2]], self.data_in_db[freq_type][self.rt60[freq_type][2]], 'yo')
        ax.plot(self.times[self.rt60[freq_type][3]], self.data_in_db[freq_type][self.rt60[freq_type][3]], 'ro')

    def plot_freqs(self, ax, freq_type="Low"):
        if freq_type not in self.data_in_db:
            print(f"Invalid frequency type: {freq_type}")
            return

        ax.clear()

        ax.plot(self.times, self.data_in_db[freq_type])
        self.plot_rt60(ax, freq_type)
        
        ax.set_title(f"Reverb {freq_type} Frequency")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")

    def plot_freqs_combined(self, ax):
        ax.clear()

        interpolated_power_low = np.interp(self.times,
                                       np.linspace(0, self.get_duration(), num=len(self.data_in_db["Low"])),
                                       self.data_in_db["Low"])

        interpolated_power_mid = np.interp(self.times,
                                       np.linspace(0, self.get_duration(), num=len(self.data_in_db["Mid"])),
                                       self.data_in_db["Mid"])

        interpolated_power_high = np.interp(self.times,
                                       np.linspace(0, self.get_duration(), num=len(self.data_in_db["High"])),
                                       self.data_in_db["High"])

        ax.plot(self.times, interpolated_power_low)
        self.plot_rt60(ax, "Low")
            
        ax.plot(self.times, interpolated_power_mid)
        self.plot_rt60(ax, "Mid")
        
        ax.plot(self.times, interpolated_power_high)
        self.plot_rt60(ax, "High")
        
        ax.set_title(f"Reverb Frequency (Combined)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")

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

