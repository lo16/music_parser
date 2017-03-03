from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    start_time = time.time()
    # Import the sample audio file and extract features
    [Fs, x] = audioBasicIO.readAudioFile("Koi_single_channel.wav")
    F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05*Fs, 0.0025*Fs)

    # Plot the general plot of ZCR and energy!
    plt.subplot(2,1,1)
    plt.plot(F[0,:])
    plt.xlabel('Frame no')
    plt.ylabel('ZCR')
    plt.subplot(2,1,2)
    plt.plot(F[1,:])
    plt.xlabel('Frame no')
    plt.ylabel('Energy')

    plt.show()

    # Extract chromagram
        specgram, time_axis, freq_axis = audioFeatureExtraction.stSpectogram(x, Fs, round(Fs *0.04), round(Fs * 0.04), True)

    # Extract chromagram
         specgram, time_axis, freq_axis = audioFeatureExtraction.stChromagram(x, Fs, round(Fs *0.04), round(Fs * 0.04), True)

    print str(time.time() - start_time) + " seconds"
