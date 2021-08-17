from PIL import Image
import math

image = Image.open('cher.bmp')
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей
image2 = Image.open('result.bmp')

pix2 = image2.load()  # Выгружаем значения пикселей

sum = 0
for x in range(width):
    for y in range(height):
        sum = sum + (int(pix[x,y][0]) - int(pix2[x,y][0]))**2 + (int(pix[x,y][1]) - int(pix2[x,y][1]))**2 + (int(pix[x,y][2]) - int(pix2[x,y][2]))**2

mse = sum/(width*height*3)
psnr = 10*math.log10((255**2)/((mse)))

print("MSE - ", mse)
print("PSNR - ", psnr)

