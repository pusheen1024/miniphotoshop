from PIL import Image, ImageDraw
from math import ceil


print('Добро пожаловать в Минифотошоп!')
filename = input('Введите название изображения в формате jpg, которое вам нужно обработать: ')
res = input('Под каким именем Вам нужно сохранить готовое изображение? ')
choice = input('''Вы хотите: 1) сделать изображение витражным;
2) Наложить на изображение радужный фильтр?\n''')
while choice != '1' and choice != '2':
    print('Пожалуйста, введите корректный ответ.')
    choice = input()
choice = int(choice)
with Image.open(filename + '.jpg') as image:
    x, y = image.size


def vitrage(pixels, i, j):
    """Transforms the image into a vitrage alike the 'Find the edges' instrument"""
    r, g, b = pixels[i, j]
    if 1 <= i < x - 1:
        r1, g1, b1 = pixels[i - 1, j]
        if abs(r - r1) <= 40 and abs(g - g1) <= 40 and abs(b - b1) <= 40:
            pixels[i - 1, j] = r, g, b
        r2, g2, b2 = pixels[i + 1, j]
        if abs(r - r2) <= 40 and abs(g - g2) <= 40 and abs(b - b2) <= 40:
            pixels[i + 1, j] = r, g, b
        else:
            pixels[i, j] = 0, 0, 0
    if 1 <= j < y - 1:
        r1, g1, b1 = pixels[i, j - 1]
        if abs(r - r1) <= 40 and abs(g - g1) <= 40 and abs(b - b1) <= 40:
            pixels[i, j - 1] = r, g, b
        r2, g2, b2 = pixels[i, j + 1]
        if abs(r - r2) <= 40 and abs(g - g2) <= 40 and abs(b - b2) <= 40:
            pixels[i, j + 1] = r, g, b
        else:
            pixels[i, j] = 0, 0, 0
    return r, g, b


def create_rainbow():
    rainbow = Image.new("RGB", (x, y), (0, 0, 0))
    canvas = ImageDraw.Draw(rainbow)
    n = ceil(y / 1024)
    for g in range(256):
        canvas.line((0, n * g, x, n * g), (255, g, 0), width=n)
    for r in range(256):
        canvas.line((0, n * (256 + r), x, n * (256 + r)), fill=(255 - r, 255, 0), width=n)
    for b in range(256):
        canvas.line((0, n * (512 + b), x, n * (512 + b)), fill=(0, 255, b), width=n)
    for g in range(256):
        canvas.line((0, n * (768 + g), x, n * (768 + g)), fill=(0, 255 - g, b), width=n)
    return rainbow


storage = list()


def rainbow_check(func):
    if not storage:
        rainbow_obj = create_rainbow()
        storage.append(rainbow_obj)
    else:
        rainbow_obj = storage[0]
    return func


@rainbow_check
def rainbow(pixels, i, j):
    """Adds a rainbow effect to an image"""
    pixels_1 = storage[0].load()
    r, g, b = pixels[i, j]
    r_1, g_1, b_1 = pixels_1[i, j]
    r = int(0.6 * r + 0.4 * r_1)
    g = int(0.6 * g + 0.4 * g_1)
    b = int(0.6 * b + 0.4 * b_1)
    return r, g, b


def main(filename, res, choice):
    with Image.open(filename) as image:
        x, y = image.size
        pixels = image.load()
        for i in range(x):
            for j in range(y):
                if choice == 1:
                    vitrage(pixels, i, j)
                elif choice == 2:
                    pixels[i, j] = rainbow(pixels, i, j)
        image.show()
        image.save(res + '.jpg')


main(filename + '.jpg', res, choice)
print('Спасибо за использование программы!')