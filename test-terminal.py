from model import Model
import matplotlib.pyplot as plt
file1 = "testConversion.mp3"
file2 = "test2.wav"
file3 = "test.wav"
print("Test 1: " + str(file1))
test1 = Model(file1)
print("Sample Rate: " + str(test1.sample_rate))
print("Length: " + str(test1.get_duration()) + " seconds")
test1.plot_waveform()

print("Test 2: " + str(file2))
test2 = Model(file2)
print("Sample Rate: " + str(test2.sample_rate))
print("Length: " + str(test2.get_duration()) + " seconds")
test2.plot_waveform()
test2.plot_freqs()

print("Test 3: " + str(file3))
test3 = Model(file3)
print("Sample Rate: " + str(test3.sample_rate))
print("Length: " + str(test3.get_duration()) + " seconds")
test3.plot_waveform()
test3.plot_freqs()
