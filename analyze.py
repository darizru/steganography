from PIL import Image

image = Image.open('cher.bmp')
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

number = 0
for x in range(width):
    for y in range(height):
        r = pix[x, y][0] % 2
        g = pix[x, y][1] % 2
        b = pix[x, y][2] % 2

        pix[x, y] = (255*r, 255*g, 255*b)

image.save("analyze_im.bmp", "BMP")



