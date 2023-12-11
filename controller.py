import tkinter as tk
from model import Model
from view import AudioAnalyzerGUI
#Creates a model using the model file and uses it to create a GUI from which the user can interact
class Controller:
    def __init__(self):
        self.model = Model()

        self.root = tk.Tk()
        self.app = AudioAnalyzerGUI(self.root, self.model)
        self.root.mainloop()

if __name__ == "__main__":
    Controller()