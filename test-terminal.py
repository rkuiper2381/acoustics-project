from model import Model
import matplotlib.pyplot as plt
file1 = "testConversion.mp3"
file2 = "test2.wav"
print("Test 1: " + str(file1))
test1 = Model(file1)
print("Sample Rate: " + str(test1.sample_rate))
print("Length: " + str(test1.get_duration()) + " seconds")
test1.plot_waveform()
test1.plot_freqs()

print("Test 2: " + str(file2))
test2 = Model(file2)
print("Sample Rate: " + str(test2.sample_rate))
print("Length: " + str(test2.get_duration()) + " seconds")
test2.plot_waveform()
test2.plot_freqs()

