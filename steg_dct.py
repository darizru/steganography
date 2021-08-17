import numpy as np
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from numpy import r_
from scipy.fftpack import fft
import imageio
import math
from functions2 import mes_out, mes_out2, steg_index, dct2, idct2, s_to_bin, bin_to_s, hamming2

def mes_in(container, mes):
    number = 0
    exit_f = False
    for i in range(8):
        for j in range(8):
            if (number < len(mes)) and (steg_index[i, j] == 1):
                if (container[i, j]%2) != int(mes[number]):
                    if container[i, j] >= 0:
                        container[i, j] = container[i, j] + 1
                    else:
                        container[i, j] = container[i, j] - 1
                number += 1
            #container[i, j] = container[i, j]*200
            if number == len(mes):
                exit_f = True
                break
        if exit_f:
            break


image = Image.open('cher.bmp')
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту

ibmp = image.convert('RGB')
(r, g, b) = ibmp.split()

r.save("imR.bmp", "BMP")
g.save("imG.bmp", "BMP")
b.save("imB.bmp", "BMP")

imr = imageio.imread('imR.bmp').astype(float)
img = imageio.imread('imG.bmp').astype(float)
imb = imageio.imread('imB.bmp').astype(float)

imsize = imr.shape
dct_r = np.zeros(imsize)
dct_mes_r = np.zeros(imsize)
im_dct_mes_r = np.zeros(imsize)
dct_g = np.zeros(imsize)
dct_mes_g = np.zeros(imsize)
im_dct_mes_g = np.zeros(imsize)
dct_b = np.zeros(imsize)
dct_mes_b = np.zeros(imsize)
im_dct_mes_b = np.zeros(imsize)

str_end = "00000000000000000000000000000000"


f1 = open('text.txt', 'r', encoding='utf-8')
message = f1.read()

f1.close()

#message = "стеганография и криптография"
b_message = s_to_bin(message) + str_end
#b_message = str_to_ascii_bin(b_message)

print("message:       ", message)
print("message_binary:",b_message)

b_len = len(b_message)
k = np.sum(steg_index)
for i in r_[:imsize[0]:8]:
    for j in r_[:imsize[1]:8]:
        dct_r[i:(i + 8), j:(j + 8)] = np.rint(dct2(imr[i:(i + 8), j:(j + 8)])).astype(int)
        dct_g[i:(i + 8), j:(j + 8)] = np.rint(dct2(img[i:(i + 8), j:(j + 8)])).astype(int)
        dct_b[i:(i + 8), j:(j + 8)] = np.rint(dct2(imb[i:(i + 8), j:(j + 8)])).astype(int)

        dct_mes_r[i:(i + 8), j:(j + 8)] = dct_r[i:(i + 8), j:(j + 8)]

        dct_mes_g[i:(i + 8), j:(j + 8)] = dct_g[i:(i + 8), j:(j + 8)]
        dct_mes_b[i:(i + 8), j:(j + 8)] = dct_b[i:(i + 8), j:(j + 8)]


        if len(b_message) > 0:
            mes = b_message[:k]
            mes_in(dct_mes_r[i:(i+8), j:(j+8)], mes)
            mes_in(dct_mes_g[i:(i + 8), j:(j + 8)], mes)
            mes_in(dct_mes_b[i:(i + 8), j:(j + 8)], mes)
            b_message = b_message[k:]

        im_dct_mes_r[i:(i + 8), j:(j + 8)] = np.rint(idct2(dct_mes_r[i:(i + 8), j:(j + 8)])).astype(int)
        im_dct_mes_g[i:(i + 8), j:(j + 8)] = np.rint(idct2(dct_mes_g[i:(i + 8), j:(j + 8)])).astype(int)
        im_dct_mes_b[i:(i + 8), j:(j + 8)] = np.rint(idct2(dct_mes_b[i:(i + 8), j:(j + 8)])).astype(int)

for i in range(imsize[0]): #проверка корректности
    for j in range(imsize[1]):
        if (im_dct_mes_b[i, j] > 255):
            im_dct_mes_b[i, j] = 255
        if (im_dct_mes_g[i, j] > 255):
            im_dct_mes_g[i, j] = 255
        if (im_dct_mes_r[i, j] > 255):
            im_dct_mes_r[i, j] = 255
        if (im_dct_mes_b[i, j] < 0):
            im_dct_mes_b[i, j] = 0
        if (im_dct_mes_g[i, j] < 0):
            im_dct_mes_g[i, j] = 0
        if (im_dct_mes_r[i, j] < 0):
            im_dct_mes_r[i, j] = 0


im_dct_mes_r = np.rint(im_dct_mes_r).astype(np.uint8)
im_dct_mes_g = np.rint(im_dct_mes_g).astype(np.uint8)
im_dct_mes_b = np.rint(im_dct_mes_b).astype(np.uint8)

img1 = Image.fromarray(im_dct_mes_r)
img2 = Image.fromarray(im_dct_mes_g)
img3 = Image.fromarray(im_dct_mes_b)

ibmp_new = Image.merge('RGB', (img1, img2, img3))
ibmp_new.save("result.bmp", "BMP")

message_red = ""
message_green = ""
message_blue = ""
message_sum = ""

exit_f = False
for i in r_[:imsize[0]:8]:
    for j in r_[:imsize[1]:8]:
        message_red += mes_out(np.rint(dct2(im_dct_mes_r[i:(i + 8), j:(j + 8)])))
        message_green += mes_out(np.rint(dct2(im_dct_mes_g[i:(i + 8), j:(j + 8)])))
        message_blue += mes_out(np.rint(dct2(im_dct_mes_b[i:(i + 8), j:(j + 8)])))
        message_sum += mes_out2(np.rint(dct2(im_dct_mes_r[i:(i + 8), j:(j + 8)])), np.rint(dct2(im_dct_mes_g[i:(i + 8), j:(j + 8)])), np.rint(dct2(im_dct_mes_b[i:(i + 8), j:(j + 8)])))
        if (len(message_sum) > 32) and (hamming2(message_sum[-32:], str_end) <= 8):
            exit_f = True
            message_red = message_red[:len(message_red)-(len(message_red)%8)]
            message_green = message_green[:len(message_green)-(len(message_green)%8)]
            message_blue = message_blue[:len(message_blue)-(len(message_blue )%8)]
            message_sum = message_sum[:len(message_sum)-(len(message_sum)%8)]
            break
    if exit_f:
        break

print("\nresult:")
print("message_red:   ", message_red)
print("message_green: ", message_green)
print("message_blue:  ", message_blue)
print("message_sum:   ", message_sum)

print("message_sum:   ", len(message_sum))

print("message_red:   ", bin_to_s(message_red))
print("message_green: ", bin_to_s(message_green))
print("message_blue:  ", bin_to_s(message_blue))
print("message_sum:   ", bin_to_s(message_sum))
