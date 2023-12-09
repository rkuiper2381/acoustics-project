import tkinter as tk
from tkinter import filedialog
import numpy as np
from model import Model
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Analyzer")

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

        self.duration_label = tk.Label(root, text="Duration: ")
        self.duration_label.pack()

        self.resonance_label = tk.Label(root, text="Highest Resonance Frequency: ")
        self.resonance_label.pack()

        # Initialize audio_model attribute
        self.audio_model = None

        # Matplotlib figure and canvas
        self.figure, self.ax = Model.create_empty_plot()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

        # State variable to keep track of the current frequency to display
        self.current_freq = "Low"

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            self.audio_model = Model(file_path)
            self.file_label.config(text=f"File: {file_path}")

            # Display the duration of the loaded audio file
            duration_seconds = self.audio_model.get_duration()
            self.duration_label.config(text=f"Duration: {duration_seconds:.2f} seconds")

            # Attempt to compute and display the highest resonance frequency
            try:
                self.audio_model.compute_highest_resonance()
                highest_resonance = self.audio_model.highest_resonance_frequency
                if highest_resonance is not None:
                    self.resonance_label.config(text=f"Highest Resonance Frequency: {highest_resonance:.2f} Hz")
                else:
                    self.resonance_label.config(text="Highest Resonance Frequency: N/A")
            except Exception as e:
                print(f"Error during highest resonance frequency computation: {e}")
                self.resonance_label.config(text="Highest Resonance Frequency: N/A")

    def display_waveform(self):
        if hasattr(self, 'audio_model'):
            self.ax.clear()
            self.audio_model.plot_waveform(self.ax)
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    def cycle_display_freqs(self):
        if self.audio_model:
            self.ax.clear()
            if self.current_freq == "Low":
                self.audio_model.plot_freqs(self.ax, "Low")
                self.current_freq = "Mid"
            elif self.current_freq == "Mid":
                self.audio_model.plot_freqs(self.ax, "Mid")
                self.current_freq = "High"
            else:
                self.audio_model.plot_freqs(self.ax, "High")
                self.current_freq = "Low"
            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")

    def combine_frequencies(self):
        if self.audio_model:
            self.ax.clear()

            # Get the data for low, mid, and high frequencies
            low_data = self.audio_model.get_data_by_frequency()["Low"]
            mid_data = self.audio_model.get_data_by_frequency()["Mid"]
            high_data = self.audio_model.get_data_by_frequency()["High"]

            # Interpolate the frequency data to match the length of the times array
            low_interp = np.interp(self.audio_model.times,
                                   np.linspace(0, self.audio_model.get_duration(), len(low_data)), low_data)
            mid_interp = np.interp(self.audio_model.times,
                                   np.linspace(0, self.audio_model.get_duration(), len(mid_data)), mid_data)
            high_interp = np.interp(self.audio_model.times,
                                    np.linspace(0, self.audio_model.get_duration(), len(high_data)), high_data)

            # Plot low, mid, and high frequencies on the same plot with distinct labels
            self.ax.plot(self.audio_model.times, low_interp, label="Low")
            self.ax.plot(self.audio_model.times, mid_interp, label="Mid")
            self.ax.plot(self.audio_model.times, high_interp, label="High")

            # Add legend with distinct labels
            self.ax.legend()

            self.ax.set_title("Combined Frequencies")
            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Power (dB)")

            self.canvas.draw_idle()
        else:
            print("No file loaded. Please load an audio file.")
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioAnalyzerGUI(root)
    root.mainloop()