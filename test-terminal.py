from model import Model
import matplotlib.pyplot as plt

test = Model("testConversion.mp3")
test2 = Model("test2.wav")
print(test.sample_rate)
print(test.get_duration())
test.plot_waveform()
test2.plot_waveform()
