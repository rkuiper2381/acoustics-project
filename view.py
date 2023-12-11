import tkinter as tk
from tkinter import filedialog
import numpy as np
from model import Model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioAnalyzerGUI:
    #init sets up the GUI and all of the buttons and empty canvas that will be later used
    def __init__(self, root, model):
        self.root = root
        self.root.title("Audio Analyzer")

        self.model = model

        # Labels and buttons on the left
        self.file_label = tk.Label(root, text="No File Loaded")
        self.file_label.grid(row=0, column=0, sticky="w")

        self.load_button = tk.Button(root, text="Load Audio File", command=self.load_file)
        self.load_button.grid(row=1, column=0, sticky="w")

        self.display_button = tk.Button(root, text="Display Waveform", command=self.display_waveform)
        self.display_button.grid(row=2, column=0, sticky="w")

        self.freqs_button = tk.Button(root, text="Display Frequencies", command=self.cycle_display_freqs)
        self.freqs_button.grid(row=3, column=0, sticky="w")

        self.combine_freqs_button = tk.Button(root, text="Combine Frequencies", command=self.combine_frequencies)
        self.combine_freqs_button.grid(row=4, column=0, sticky="w")

        self.display_button = tk.Button(root, text="Display Resonance", command=self.display_resonance)
        self.display_button.grid(row=5, column=0, sticky="w")

        self.duration_label = tk.Label(root, text="Duration: ")
        self.duration_label.grid(row=6, column=0, sticky="w")

        self.resonance_label = tk.Label(root, text="Highest Resonance Frequency: ")
        self.resonance_label.grid(row=7, column=0, sticky="w")

        self.rt60_low_label = tk.Label(root, text="RT60 Low: N/A")
        self.rt60_low_label.grid(row=8, column=0, sticky="w")

        self.rt60_mid_label = tk.Label(root, text="RT60 Mid: N/A")
        self.rt60_mid_label.grid(row=9, column=0, sticky="w")

        self.rt60_high_label = tk.Label(root, text="RT60 High: N/A")
        self.rt60_high_label.grid(row=10, column=0, sticky="w")

        self.rt60_avg_label = tk.Label(root, text="RT60 Average: N/A")
        self.rt60_avg_label.grid(row=11, column=0, sticky="w")

        self.rt60_avg_minus_5_label = tk.Label(root, text="RT60 Average - 5: N/A")
        self.rt60_avg_minus_5_label.grid(row=12, column=0, sticky="w")

        self.rt60_label = tk.Label(root, text="RT60 Differences: N/A")
        self.rt60_label.grid(row=13, column=0, sticky="w")

        # Matplotlib figure and canvas on the right
        self.figure, self.ax = Model.create_empty_plot()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=14)

        # State variable to keep track of the current frequency to display
        self.current_freq = "Low"

    #load file allows a user to select a mp3 or wav file and upload it
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            #Below takes info that can all be displayed at the same time (doesn't require a plot) and displays that data on the GUI
            self.model.load_file(file_path)
            resonance = self.model.get_resonance()
            print(f"Resonance is {resonance} Hz")
            self.file_label.config(text=f"File: {file_path}")

            # Display the duration of the loaded audio file
            duration_seconds = self.model.get_duration()
            self.duration_label.config(text=f"Duration: {duration_seconds:.2f} seconds")

            # Attempt to compute and display the highest resonance frequency
            self.resonance_label.config(text=f"Resonance Frequency: {resonance:.2f} Hz")

            # Calculate RT60 for each frequency band
            rt60_data = self.model.calc_rt60()

            # Extract values for each frequency band
            rt60_low = rt60_data["Low"][0][0]
            rt60_mid = rt60_data["Mid"][0][0]
            rt60_high = rt60_data["High"][0][0]

            # Calculate averages
            rt60_avg = self.model.get_rt60()
            rt60_avg_minus_5 = rt60_avg - .5

            rt60_low_text = f"RT60 Low: {rt60_low:.2f} seconds"
            rt60_mid_text = f"RT60 Mid: {rt60_mid:.2f} seconds"
            rt60_high_text = f"RT60 High: {rt60_high:.2f} seconds"
            rt60_avg_text = f"RT60 Average: {rt60_avg:.2f} seconds"
            rt60_avg_minus_5_text = f"RT60 Average - 0.5: {rt60_avg_minus_5:.2f} seconds"
            rt60_diff_text = f"RT60 Differences: Low-Mid: {rt60_mid - rt60_low:.2f}, Mid-High: {rt60_high - rt60_mid:.2f}, High-Low: {rt60_low - rt60_high:.2f}"
            self.rt60_label.config(text=rt60_diff_text)
            self.rt60_low_label.config(text=rt60_low_text)
            self.rt60_mid_label.config(text=rt60_mid_text)
            self.rt60_high_label.config(text=rt60_high_text)
            self.rt60_avg_label.config(text=rt60_avg_text)
            self.rt60_avg_minus_5_label.config(text=rt60_avg_minus_5_text)

    #displays the resonance plot upon button press
    def display_resonance(self):
        if hasattr(self, 'model') and self.model:
            self.ax.clear()
            self.model.plot_resonance(self.ax)
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    # displays the waveform plot upon button press
    def display_waveform(self):
        if hasattr(self, 'model') and self.model:
            self.ax.clear()
            self.model.plot_waveform(self.ax)
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    #displays the RT60 reverb / freq plot cyclicly upon button press
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

    #Displays the combined plot upon button press
    def combine_frequencies(self):
        if self.model:
            self.ax.clear()

            self.model.plot_freqs_combined(self.ax)
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")
