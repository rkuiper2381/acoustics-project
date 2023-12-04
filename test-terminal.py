from model import Model
import matplotlib.pyplot as plt

test = Model("test.wav")
test2 = Model("test2.wav")
print(test.sample_rate)
print(test.get_duration())
test.plot_waveform()
test2.plot_waveform()
