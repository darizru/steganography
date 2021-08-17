import numpy as np
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from numpy import r_
from scipy.fftpack import fft

def dct2(a):
    return scipy.fftpack.dct(scipy.fftpack.dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

def idct2(a):
    return scipy.fftpack.idct(scipy.fftpack.idct(a, axis=0, norm='ortho'), axis=1, norm='ortho')

def hamming2(s1, s2):
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def s_to_bin(string):
    return ''.join([bin(int(c.encode('cp1251').hex(), 16))[2:].zfill(8) for c in string])

def bin_to_s(_str):
    out = [_str[i:i+8] for i in range(0, len(_str), 8)]
    return ''.join([bytes([int(item, 2)]).decode('cp1251') for item in out])


steg_index = np.array([[0, 0, 0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 1, 1, 0, 0],
                       [0, 0, 0, 0, 1, 1, 0, 0],
                       [0, 0, 1, 1, 0, 0, 0, 0],
                       [0, 0, 1, 1, 0, 0, 0, 0],
                       [1, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])

steg_index2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 1, 1, 1, 0, 0],
                       [0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])

steg_index3 = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])

def mes_out(container):
    message = ""
    exit_f = False
    for i in range(8):
        for j in range(8):
            if steg_index[i, j] == 1:
                message += str(int(np.trunc((container[i, j]))) % 2)


    return message

def mes_out2(container1, container2, container3):
    message = ""
    ''''''
    for i in range(8):
        for j in range(8):
            if steg_index[i, j] == 1:
                sum = (int(np.trunc((container1[i, j]))) % 2) + (int(np.trunc((container2[i, j]))) % 2) + (int(np.trunc((container3[i, j]))) % 2)
                if sum > 1:
                    message += "1"
                else:
                    message += "0"
    return message
