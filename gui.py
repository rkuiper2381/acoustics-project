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

        self.rt60_button = tk.Button(root, text="Display RT60 Info", command=self.display_rt60_info)
        self.rt60_button.pack()

        self.duration_label = tk.Label(root, text="Duration: ")
        self.duration_label.pack()

        self.resonance_label = tk.Label(root, text="Highest Resonance Frequency: ")
        self.resonance_label.pack()

        self.rt60_low_label = tk.Label(root, text="RT60 Low: N/A")
        self.rt60_low_label.pack()

        self.rt60_mid_label = tk.Label(root, text="RT60 Mid: N/A")
        self.rt60_mid_label.pack()

        self.rt60_high_label = tk.Label(root, text="RT60 High: N/A")
        self.rt60_high_label.pack()

        self.rt60_avg_label = tk.Label(root, text="RT60 Average: N/A")
        self.rt60_avg_label.pack()

        self.rt60_avg_minus_5_label = tk.Label(root, text="RT60 Average - 5: N/A")
        self.rt60_avg_minus_5_label.pack()

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
            #self.model.plot_resonance(self.ax)
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

            self.model.plot_freqs_combined(self.ax)
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    def display_rt60_info(self):
        if self.model:
            # Calculate RT60 for each frequency band
            rt60_data = self.model.calc_rt60()

            # Extract values for each frequency band
            rt60_low = rt60_data["Low"][0][0]
            rt60_mid = rt60_data["Mid"][0][0]
            rt60_high = rt60_data["High"][0][0]

            # Calculate averages
            rt60_avg = self.model.get_rt60()
            rt60_avg_minus_5 = rt60_avg - 5


            rt60_low_text = f"RT60 Low: {rt60_low:.2f} seconds"
            rt60_mid_text = f"RT60 Mid: {rt60_mid:.2f} seconds"
            rt60_high_text = f"RT60 High: {rt60_high:.2f} seconds"
            rt60_avg_text = f"RT60 Average: {rt60_avg:.2f} seconds"
            rt60_avg_minus_5_text = f"RT60 Average - 5: {rt60_avg_minus_5:.2f} seconds"
            rt60_diff_text = f"RT60 Differences: Low-Mid: {rt60_mid - rt60_low:.2f}, Mid-High: {rt60_high - rt60_mid:.2f}, High-Low: {rt60_low - rt60_high:.2f}"
            self.rt60_label.config(text=rt60_diff_text)
            self.rt60_low_label.config(text=rt60_low_text)
            self.rt60_mid_label.config(text=rt60_mid_text)
            self.rt60_high_label.config(text=rt60_high_text)
            self.rt60_avg_label.config(text=rt60_avg_text)
            self.rt60_avg_minus_5_label.config(text=rt60_avg_minus_5_text)

        else:
            print("No file loaded. Please load an audio file.")