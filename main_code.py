"""
Main code to process files from mfcc to an output dct for clustering analysis
"""
# Pyaudio packages
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from pydub import AudioSegment
from joblib import Parallel, delayed

# Core analysis packages
import matplotlib.pyplot as plt
import numpy as np 
from scipy.fftpack import dct
import pickle
import time
import os


def mfcc_extraction(song, win_buf=0.050, step_buf=0.025):
    """Extracts a MFCC from a wav file
    Args:
        song (string): path to a song name
        win_buff (float): multiplier on samp freq to determine window size
        step_buff (float): multiplier on samp freq to determine step size
    Returns:
        mfcc (np array): array containing MFCC corresponding with input song
    """
    # Feature extraction using single channel conversion
    # to use a stereo copy, average the two channels
    # Get the sampling frequency and the converted audio file
    [fs, x] = audioBasicIO.readAudioFile(song);

    # Take in params to modify sample length
    fts = audioFeatureExtraction.stFeatureExtraction(x, fs, win_buf*fs, step_buf*fs);

    # Retrieve MFCCs from the feature set and take the transpose for convenience
    mfcc = np.array(fts[8:20]).T

    return mfcc

def calc_dist_matrix(mfcc):
    """Calculates distance matrix based on MFCC
    Args:
        mfcc (np array): array containing the MFCC of a song
    Returns:
        dist_matrix (list of lists): list containing the distribution matrix in list of lists
    """
    # calculate distance matrix (VERY, VERY EXPENSIVE)
    # TODO: optimize this algorithm
    dist_matrix = [Parallel(n_jobs=3, backend="threading")(delayed(np.linalg.norm)(mfcc[i] - mfcc[j]) for j in xrange(len(mfcc))) for i in xrange(len(mfcc))]
    #dist_matrix = [Parallel(n_jobs=3, backend="multiprocessing")(delayed(np.linalg.norm)(mfcc[i] - mfcc[j]) for j in xrange(len(mfcc))) for i in xrange(len(mfcc))]
    return dist_matrix

def beat_spectrum(dist_matrix, fps=40):
    """Calculates the audio beat spectra
    Args:
        dist_matrix (list of lists): list of lists containing the distance matrix
        fps (int): the number of frames we take per second
    Returns:
        spec (list): beat spectrum corresponding to the distance matrix
    """
    # Determine the total number of frames
    total_frames = len(dist_matrix)

    # Select window parameters to determine window to sum over
    # R determines the size of the window, m determines where the window starts
    R = int(4.75 * fps)
    m = int(2.5 * fps)

    # l is tentatively set to 3
    # l is the num off diagonal we are referring to
    l = int(3 * fps)

    # We drop the first part of the sample to reduce noise
    throwOut = 0.125 * fps

    # Go through while loop to sum for each window
    spec = []
    currM = 0
    currB = 0
    while currM < (total_frames - R - l):
	spectrum = [dist_matrix[i][i+l] for i in xrange((int)(currM + throwOut) , (int)(currM + R))]
	spec.append(sum(spectrum))
	currM += m

	print currM, total_frames, currM + R + l

    return spec


def get_dct(spec):
    """Returns the dct of the input spectrum
    Args:
        spec (list): list containing the spectrum of a song
    Returns:
        dcost (np array): the dct of the input sectrum
    """
    # Use scipy's dct function to process the spectra
    dcost = dct(spec, n=50)[:13]

    return dcost

def process(song):
    """Core function that processes individual songs
    Args:
        song (string): name of song file; must be mono wav
    Returns:
        mfcc (np array): returns the mfcc of the song
        dist_matrix (list of lists): returns the distance matrix
        spec (list): returns the list containing the spectrum
        song_dct (np array): returns the numpy array of the DCT
    """
    start = time.time()

    # Run the process mfcc -> dist matrix -> spec -> dct
    mfcc = mfcc_extraction(song, 0.050, 0.025)
    dist_matrix = calc_dist_matrix(mfcc)
    spec = beat_spectrum(dist_matrix, 40.)
    song_dct = get_dct(spec)

    end = time.time()

    print "%s took %s seconds to process!" %(song, str(end - start))

    return mfcc, dist_matrix, spec, song_dct


def plot(mfcc, dist_matrix, spec, song_dct):
    """Plot relevant graphs for examination
    Args:
        mfcc (np array): the mfcc of the song
        dist_matrix (list of lists): the distance matrix
        spec (list): the list containing the spectrum
        song_dct (np array): the numpy array of the DCT
    """
    # Plot the beat spectra
    fig, ax = plt.subplots(figsize=(200,200))
    ax.plot(song_dct)
    ax.grid(True)
    plt.title('Beat Spectrum')
    plt.show()

    # Plot the distance matrix
    fig, ax = plt.subplots(figsize=(200,200))
    cax = ax.matshow(dist_matrix, cmap='viridis', interpolation='nearest')
    ax.grid(True)
    plt.title('MFCC similarity matrix')
    plt.show()

def wav_check(root, song):
    """Checks if song is wav, and converts wav files. Requires FFmpeg!
    Args:
        root (string): root folder of file
        song (string): song name
    Returns:
        wav_filename (string): if success, returns name of new wav file
        song (string): returns the original song name if already wav
    """
    # Convert if song isn't already a wav file
    if song.split('.')[-1] != 'wav':
        # Path to store to
	wav_filename = os.path.splitext(os.path.basename(song))[0] + '.wav'
	wav_filename = os.path.join(root, wav_filename)

	# Convert to wav file
	sound = AudioSegment.from_file(song, format=song.split('.')[-1])
	sound = sound.set_channels(1)
	sound.export(wav_filename, format='wav').close()
        
        # End conversion and return
	return wav_filename
    
    # Otherwise, return the original file
    return song

if __name__ == '__main__':
    #1. iterate over each audio file
    #2. check if file is WAV. if not, convert to mono
    #3. extract MFCC
    #4. calculate distance matrix
    #5. get beat spectrum
    #6. get DCT
    #7. add DCT to list of DCTs
    #8. when all songs are added, dump list to pickle

    DCTs = []
    directory = 'D:\\music\\current playlist\\a5'
    #step 1
    for root, dirs, files in os.walk(directory):
        for file in files:
            file = os.path.join(root, file)

            try:
                #step 2
    		file = wav_check(root, file)
                #steps 3-7
                mfcc, dm, spec, dct = process(file)
    		DCTs.append(dct)

                # Optional plotting
                # plot(mfcc, dm, spec, dct)
            except:
		pass

	#step 8
	f = open('DCTs.p', 'wb')
	pickle.dump(DCTs, f)
	f.close()

