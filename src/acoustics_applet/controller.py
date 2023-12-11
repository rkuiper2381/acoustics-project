import tkinter as tk
from model import Model
from gui import AudioAnalyzerGUI

class Controller:
    def __init__(self):
        self.model = Model()

        self.root = tk.Tk()
        self.app = AudioAnalyzerGUI(self.root, self.model)
        self.root.mainloop()

if __name__ == "__main__":
    Controller()