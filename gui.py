import tkinter as tk
from tkinter import filedialog
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

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioAnalyzerGUI(root)
    root.mainloop()