from model import Model
import matplotlib.pyplot as plt
file1 = "testConversion.mp3"
file2 = "test2.wav"
file3 = "test.wav"
print("Test 1: " + str(file1))
test1 = Model(file1)
print("Sample Rate: " + str(test1.sample_rate))
print("Length: " + str(test1.get_duration()) + " seconds")

test1_fig, test1_ax = Model.create_empty_plot()
test1.plot_waveform(test1_ax)
test1.plot_freqs(test1_ax)


print("Test 2: " + str(file2))
test2 = Model(file2)
print("Sample Rate: " + str(test2.sample_rate))
print("Length: " + str(test2.get_duration()) + " seconds")

test2_fig, test2_ax = Model.create_empty_plot()
test2.plot_waveform(test2_ax)
test2.plot_freqs(test2_ax)


print("Test 3: " + str(file3))
test3 = Model(file3)
print("Sample Rate: " + str(test3.sample_rate))
print("Length: " + str(test3.get_duration()) + " seconds")

test3_fig, test3_ax = Model.create_empty_plot()
test3.plot_waveform(test3_ax)
test3.plot_freqs(test3_ax)

