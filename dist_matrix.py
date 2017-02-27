from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import numpy as np 

#here I use a single channel conversion of Koi
#to use a stereo copy simply average the two channels (for now)
[Fs, x] = audioBasicIO.readAudioFile("Koi_single_channel.wav");

#TODO: tweak sample length
F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs);

#retrieve MFCCs from F and take the transpose for convenience
MFCC = np.array(F[8:20]).T

#calculate distance matrix (VERY EXPENSIVE)
dist_matrix = [[np.linalg.norm(MFCC[i] - MFCC[j]) for j in xrange(len(MFCC))] for i in xrange(len(MFCC))]
#dist_matrix = np.zeros((len(MFCC), len(MFCC)))


fig, ax = plt.subplots(figsize=(200,200))
cax = ax.matshow(dist_matrix, interpolation='nearest')
ax.grid(True)
plt.title('MFCC similarity matrix')
plt.show()