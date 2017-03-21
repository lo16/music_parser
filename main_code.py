from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import numpy as np 
from scipy.fftpack import dct
import pickle

NUM_FRAMES_PER_SECOND = 40

#input: song filename
#output: MFCC array
def mfcc_extraction(song):
	#feature extraction
	#here I use a single channel conversion of Koi
	#to use a stereo copy simply average the two channels (for now)
	[Fs, x] = audioBasicIO.readAudioFile(song);

	#TODO: tweak sample length
	F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs);

	#retrieve MFCCs from F and take the transpose for convenience
	MFCC = np.array(F[8:20]).T

	return MFCC

###############################################################################################################
def calc_dist_matrix(MFCC):
	#calculate distance matrix (VERY, VERY EXPENSIVE)
	dist_matrix = [[np.linalg.norm(MFCC[i] - MFCC[j]) for j in xrange(len(MFCC))] for i in xrange(len(MFCC))]
	return dist_matrix
	#dist_matrix = np.zeros((len(MFCC), len(MFCC)))



###############################################################################################################
#beat spectrum section
def beat_spectrum(dist_matrix):
	total_frames = len(dist_matrix)
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

	return B

###############################################################################################################
#DCT
def get_dct(B):
	return dct(B, n=50)[:13]

###############################################################################################################

# NEXT: GET DCT FOR MULTIPLE SONGS AND CLUSTER THEM

###############################################################################################################
#overall function
#input: filename (MUST BE MONO WAV)
#output: DCT of song
def process(song):
	MFCC = mfcc_extraction(song)
	dist_matrix = calc_dist_matrix(MFCC)
	B = beat_spectrum(dist_matrix)
	song_dct = get_dct(B)
	return song_dct

###############################################################################################################
# #plots
# fig, ax = plt.subplots(figsize=(200,200))
# ax.plot(B)
# ax.grid(True)
# plt.title('Beat Spectrum, R = %d sec, L = %d sec' % (R/NUM_FRAMES_PER_SECOND, l/NUM_FRAMES_PER_SECOND))
# plt.show()

# fig, ax = plt.subplots(figsize=(200,200))
# cax = ax.matshow(dist_matrix, cmap='viridis', interpolation='nearest')
# ax.grid(True)
# plt.title('MFCC similarity matrix')
# plt.show()

if __name__ == '__main__':
	# MFCC = mfcc_extraction("Koi_mono.wav")
	# dist_matrix = calc_dist_matrix(MFCC)
	# B = beat_spectrum(dist_matrix)
	# song_dct = get_dct(B)
	

	#1. iterate over each audio file
	#2. check if file is WAV. if not, convert to mono
	#3. extract MFCC
	#4. calculate distance matrix
	#5. get beat spectrum
	#6. get DCT
	#7. add DCT to list of DCTs
	#8. when all songs are added, dump list to pickle

	DCTs = []
	#step 1
	for root, dirs, files in os.walk("."):
		for file in files:
			try:
				#TODO: step 2

				#steps 3-7
				DCTs.append(process(file))
			except:
				pass

	#step 8
	f = open('DCTs.p', 'wb')
	pickle.dump(DCTs, f)
	f.close()