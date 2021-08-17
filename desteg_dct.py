import numpy as np
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from numpy import r_
from scipy.fftpack import fft
import imageio
import math
from functions import SToBin, AddLen
from functions2 import mes_out, mes_out2, steg_index, dct2, hamming2, bin_to_s, s_to_bin

image = Image.open('result.bmp')
(r, g, b) = image.split()

r.save("imR.bmp", "BMP")
g.save("imG.bmp", "BMP")
b.save("imB.bmp", "BMP")

imr = imageio.imread('imR.bmp').astype(float)
img = imageio.imread('imG.bmp').astype(float)
imb = imageio.imread('imB.bmp').astype(float)

imsize = imr.shape
dct_r = np.zeros(imsize)
dct_g = np.zeros(imsize)
dct_b = np.zeros(imsize)

message_red = ""
message_green = ""
message_blue = ""
message_sum = ""
exit_f = False
number = 0
str_end = "00000000000000000000000000000000"

for i in r_[:imsize[0]:8]:
    for j in r_[:imsize[1]:8]:
        message_red += mes_out(np.rint(dct2(imr[i:(i + 8), j:(j + 8)])))
        message_green += mes_out(np.rint(dct2(img[i:(i + 8), j:(j + 8)])))
        message_blue += mes_out(np.rint(dct2(imb[i:(i + 8), j:(j + 8)])))
        message_sum += mes_out2(np.rint(dct2(imr[i:(i + 8), j:(j + 8)])), np.rint(dct2(img[i:(i + 8), j:(j + 8)])), np.rint(dct2(imb[i:(i + 8), j:(j + 8)])))
        if (len(message_sum) > 32) and (hamming2(message_sum[-32:], str_end) <= 8):
            exit_f = True
            message_red = message_red[:len(message_red)-(len(message_red)%8)]
            message_green = message_green[:len(message_green)-(len(message_green)%8)]
            message_blue = message_blue[:len(message_blue)-(len(message_blue )%8)]
            message_sum = message_sum[:len(message_sum)-(len(message_sum)%8)]
            break
    if exit_f:
        break


print("\nmessage_red:   ", message_red)
print("message_green: ", message_green)
print("message_blue:  ", message_blue)
print("message_sum:   ", message_sum)

print("message_red:   ", bin_to_s(message_red))
print("message_green: ", bin_to_s(message_green))
print("message_blue:  ", bin_to_s(message_blue))
print("message_sum:   ", bin_to_s(message_sum))
