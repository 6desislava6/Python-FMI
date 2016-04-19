from collections import defaultdict


RGB_VALUE = 255
#VALS = [0.2126, 0.7152, 0.0722]


def grayscale(func):
    def decorated_func(*args):
        return make_gray(func(*args))
    return decorated_func


def make_gray_pixel(pix):
    c_lin = int(sum(pix) / 3)
    #c_lin = int(sum([a * b for a, b in zip(VALS, pix)]))
    return (c_lin, c_lin, c_lin)


def make_gray(image):
    return [[make_gray_pixel(image[i][j]) for j
             in range(len(image[0]))] for i in range(len(image))]


@grayscale
def rotate_right(picture):
    return [list(x) for x in zip(*picture[::-1])]


@grayscale
def rotate_left(picture):
    return [list(x) for x in zip(*picture)][::-1]


def invert_pixel(pixel):
    return (RGB_VALUE - pixel[0], RGB_VALUE - pixel[1], RGB_VALUE - pixel[2])


def lighten_pixel(pixel, coeff):
    return (int(pixel[0] + coeff * (RGB_VALUE - pixel[0])),
            int(pixel[1] + coeff * (RGB_VALUE - pixel[1])),
            int(pixel[2] + coeff * (RGB_VALUE - pixel[2])))


def darken_pixel(pixel, coeff):
    return (int(pixel[0] - coeff * (pixel[0] - 0)),
            int(pixel[1] - coeff * (pixel[1] - 0)),
            int(pixel[2] - coeff * (pixel[2] - 0)))


def change_pixels(image, func, *args):
    length_row = len(image)
    length_col = len(image[0])

    changed = [[func(image[x][y], *args) for y in range(0, length_col)]
               for x in range(0, length_row)]

    return changed


@grayscale
def invert(image):
    return change_pixels(image, invert_pixel)


@grayscale
def lighten(image, coeff):
    return change_pixels(image, lighten_pixel, coeff)


@grayscale
def darken(image, coeff):
    return change_pixels(image, darken_pixel, coeff)


def create_histogram(image):
    result = {
        'red': defaultdict(int),
        'green': defaultdict(int),
        'blue': defaultdict(int)
    }

    for line in image:
        for pixel in line:
            result['red'][pixel[0]] += 1
            result['green'][pixel[1]] += 1
            result['blue'][pixel[2]] += 1

    return result
