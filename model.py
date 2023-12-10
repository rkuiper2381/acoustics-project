import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from os import path

class Model:
    def __init__(self):
        self.file_path = None
        self.sample_rate = None
        self.data = None
        self.spectrum = None
        self.freqs = None
        self.times = None
        self.data_in_db = None
        self.highest_resonance_frequency = None

    def load_file(self, file_path):
        if file_path.endswith('.mp3'):
            sound = AudioSegment.from_mp3(file_path)
            dst = file_path.split('.')[0]
            dst = dst + '.wav'
            sound.export(dst, format='wav')
            file_path = dst
            print('mp3 file converted to wav file')

        self.file_path = self.check_metadata(file_path)
        self.sample_rate, self.data = wavfile.read(self.file_path)

        self.check_channels()
        self.data = self.data.flatten()
        self.spectrum, self.freqs, self.bins, self.img = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024,
                                                                      cmap=plt.get_cmap("autumn_r"))
        self.times = np.linspace(0, self.get_duration(), num=self.data.shape[0])
        self.data_in_db = self.get_data_by_frequency()

    @classmethod
    def create_empty_plot(cls):
        fig, ax = plt.subplots()
        ax.set_title("Empty Plot")
        ax.set_xlabel("X-axis Label")
        ax.set_ylabel("Y-axis Label")
        return fig, ax

    def check_metadata(self, file):
        sound = AudioSegment.from_file(file)

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
        if len(self.data.shape) > 1 and self.data.shape[1] > 1:
            print("Multiple channels found. Converting to single channel.")
            self.data = np.mean(self.data, axis=1)

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

    def get_data_by_frequency(self):
        x = {"Low": self.frequency_check(100),
             "Mid": self.frequency_check(1000),
             "High": self.frequency_check(5000)
             }
        return x

    def get_duration(self):
        return self.data.shape[0] / self.sample_rate

    def get_resonance(self):
        idx = np.argmax(self.spectrum) // len(self.spectrum[0])
        return self.freqs[idx]

    def plot_waveform(self, ax):
        ax.clear()
        ax.plot(self.times, self.data)
        ax.set_title("Waveform")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

    def plot_freqs(self, ax, freq_type="Low"):
        if freq_type not in self.data_in_db:
            print(f"Invalid frequency type: {freq_type}")
            return

        ax.clear()

        interpolated_power = np.interp(self.times,
                                       np.linspace(0, self.get_duration(), num=len(self.data_in_db[freq_type])),
                                       self.data_in_db[freq_type])

        ax.plot(self.times, interpolated_power)
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
        ax.plot(self.times, interpolated_power_mid)
        ax.plot(self.times, interpolated_power_high)
        ax.set_title(f"Reverb Frequency (Combined)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")