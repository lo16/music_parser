from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction

import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np 

def read_audio(file_name):
    '''
    Reads a .wav file to convert into mfcc
    Makes no folder assumptions. Please specify from root
    '''
    # here I use a single channel conversion of a wav file
    # to use a stereo copy simply average the two channels (for now)
    [fs, x] = audioBasicIO.readAudioFile(file_name)

    #TODO: tweak sample length and figure out optimal
    converted = audioFeatureExtraction.stFeatureExtraction(x, fs, 0.050*fs, 0.025*fs)

    return converted

def calc_distance(mfcc):
    '''
    Function to calculate the relative distance based on a MFCC
    We loop through and calculate the distance on all pairs i and j
    This function is very expensive
    '''
    start_time = time.time()
    dist_matrix = [[np.linalg.norm(mfcc[i] - mfcc[j]) for j in xrange(len(mfcc))] for i in xrange(len(mfcc))]
    
    print "Matrix calc time: " + str(time.time() - start_time) + " secs"

    return dist_matrix

if __name__ == "__main__":
    # Assumes we are in music_parse folder
    conv_audio = read_audio("Koi_single_channel.wav")

    #retrieve MFCCs from converted audio
    # take the transpose to realign columns
    mfcc = np.array(conv_audio[8:20]).T
    dist_matrix = calc_distance(mfcc)
    pd.DataFrame(dist_matrix).to_pickle("koi_pickle.pkl")

    # Plot the MFCC results
    plt.imshow(dist_matrix, cmap='viridis', interpolation='nearest')
    plt.title('MFCC similarity matrix')
    plt.show()
