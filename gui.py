import tkinter as tk
from tkinter import filedialog
import numpy as np
from model import Model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioAnalyzerGUI:
    def __init__(self, root, model):
        self.root = root
        self.root.title("Audio Analyzer")

        self.model = model

        self.file_label = tk.Label(root, text="No File Loaded")
        self.file_label.pack()

        self.load_button = tk.Button(root, text="Load Audio File", command=self.load_file)
        self.load_button.pack()

        self.display_button = tk.Button(root, text="Display Waveform", command=self.display_waveform)
        self.display_button.pack()

        self.freqs_button = tk.Button(root, text="Display Frequencies", command=self.cycle_display_freqs)
        self.freqs_button.pack()

        self.combine_freqs_button = tk.Button(root, text="Combine Frequencies", command=self.combine_frequencies)
        self.combine_freqs_button.pack()

        self.rt60_button = tk.Button(root, text="Display RT60 Differences", command=self.display_rt60_differences)
        self.rt60_button.pack()

        self.duration_label = tk.Label(root, text="Duration: ")
        self.duration_label.pack()

        self.resonance_label = tk.Label(root, text="Highest Resonance Frequency: ")
        self.resonance_label.pack()

        self.rt60_label = tk.Label(root, text="RT60 Differences: N/A")
        self.rt60_label.pack()

        # Matplotlib figure and canvas
        self.figure, self.ax = Model.create_empty_plot()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

        # State variable to keep track of the current frequency to display
        self.current_freq = "Low"

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            self.model.load_file(file_path)
            resonance = self.model.get_resonance()
            print(f"Resonance is {resonance}")
            self.file_label.config(text=f"File: {file_path}")

            # Display the duration of the loaded audio file
            duration_seconds = self.model.get_duration()
            self.duration_label.config(text=f"Duration: {duration_seconds:.2f} seconds")

            # Attempt to compute and display the highest resonance frequency
            self.resonance_label.config(text=f"Highest Resonance Frequency: {resonance:.2f}")

    def display_waveform(self):
        if hasattr(self, 'model') and self.model:
            self.ax.clear()
            self.model.plot_waveform(self.ax)
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    def cycle_display_freqs(self):
        if self.model:
            self.ax.clear()
            if self.current_freq == "Low":
                self.model.plot_freqs(self.ax, "Low")
                self.current_freq = "Mid"
            elif self.current_freq == "Mid":
                self.model.plot_freqs(self.ax, "Mid")
                self.current_freq = "High"
            else:
                self.model.plot_freqs(self.ax, "High")
                self.current_freq = "Low"
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    def combine_frequencies(self):
        if self.model:
            self.ax.clear()

            # Get the data for low, mid, and high frequencies
            low_data = self.model.get_data_by_frequency()["Low"]
            mid_data = self.model.get_data_by_frequency()["Mid"]
            high_data = self.model.get_data_by_frequency()["High"]

            # Interpolate the frequency data to match the length of the times array
            low_interp = np.interp(self.model.times,
                                   np.linspace(0, self.model.get_duration(), len(low_data)), low_data)
            mid_interp = np.interp(self.model.times,
                                   np.linspace(0, self.model.get_duration(), len(mid_data)), mid_data)
            high_interp = np.interp(self.model.times,
                                    np.linspace(0, self.model.get_duration(), len(high_data)), high_data)

            # Plot low, mid, and high frequencies on the same plot with distinct labels
            self.ax.plot(self.model.times, low_interp, label="Low")
            self.ax.plot(self.model.times, mid_interp, label="Mid")
            self.ax.plot(self.model.times, high_interp, label="High")

            # Add legend with distinct labels
            self.ax.legend()

            self.ax.set_title("Combined Frequencies")
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Power (dB)")

            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    def display_rt60_differences(self):
        if self.model:
            # Calculate RT60 for each frequency band
            rt60_low = self.calculate_rt60("Low")
            rt60_mid = self.calculate_rt60("Mid")
            rt60_high = self.calculate_rt60("High")

            # Display the RT60 differences in the existing GUI
            rt60_text = f"RT60 Differences (s): Low: {rt60_low:.2f}, Mid: {rt60_mid:.2f}, High: {rt60_high:.2f}"
            self.rt60_label.config(text=rt60_text)

        else:
            print("No file loaded. Please load an audio file.")

    def calculate_rt60(self, freq_type):
        if freq_type in self.model.data_in_db:
            # Find the index of the maximum value in the dB array
            max_index = np.argmax(self.model.data_in_db[freq_type])

            # Calculate values according to the guidelines
            max_value = self.model.data_in_db[freq_type][max_index]
            threshold_minus_5dB = max_value - 5
            threshold_minus_25dB = max_value - 25

            # Find the time indices corresponding to the calculated values
            index_minus_5dB = np.argmax(self.model.data_in_db[freq_type] >= threshold_minus_5dB)
            index_minus_25dB = np.argmax(self.model.data_in_db[freq_type] >= threshold_minus_25dB)

            # Convert the indices to time in seconds
            time_minus_5dB = self.model.times[index_minus_5dB]
            time_minus_25dB = self.model.times[index_minus_25dB]

            # Calculate RT60 as the time it takes amplitude to drop from max (less 5dB) to max (less 25dB)
            rt60 = (time_minus_25dB - time_minus_5dB) * 3

            print(f"RT60 for {freq_type} frequencies: {rt60:.2f} seconds")
            return rt60

        else:
            print(f"Invalid frequency type: {freq_type}")
            return 0