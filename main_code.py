from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import numpy as np 

NUM_FRAMES_PER_SECOND = 40

#here I use a single channel conversion of Koi
#to use a stereo copy simply average the two channels (for now)
[Fs, x] = audioBasicIO.readAudioFile("Koi_mono.wav");

#TODO: tweak sample length
F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs);

#retrieve MFCCs from F and take the transpose for convenience
MFCC = np.array(F[8:20]).T

#calculate distance matrix (VERY EXPENSIVE)
dist_matrix = [[np.linalg.norm(MFCC[i] - MFCC[j]) for j in xrange(len(MFCC))] for i in xrange(len(MFCC))]
#dist_matrix = np.zeros((len(MFCC), len(MFCC)))
total_frames = len(dist_matrix)

#beat spectrum section
R = 4.75 * NUM_FRAMES_PER_SECOND
m = 2.5 * NUM_FRAMES_PER_SECOND

#l is tentatively set to 3
l = 3 * NUM_FRAMES_PER_SECOND
throwOut = 0.125 * NUM_FRAMES_PER_SECOND
B = []

currM = 0
currB = 0
while currM < (total_frames - R - l):
	spectrum = [dist_matrix[i][i+l] for i in xrange((int)(currM + throwOut) , (int)(currM + R))]
	B.append(sum(spectrum))
	currM += m
	print currM, total_frames, currM + R + l

fig, ax = plt.subplots(figsize=(200,200))
ax.plot(B)
ax.grid(True)
plt.title('Beat Spectrum, R = %d sec, L = %d sec' % (R/NUM_FRAMES_PER_SECOND, l/NUM_FRAMES_PER_SECOND))
plt.show()

fig, ax = plt.subplots(figsize=(200,200))
cax = ax.matshow(dist_matrix, cmap='viridis', interpolation='nearest')
ax.grid(True)
plt.title('MFCC similarity matrix')
plt.show()

