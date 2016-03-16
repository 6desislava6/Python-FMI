from collections import defaultdict

DIRECTIONS = {
    'left': lambda x, y, length: [y, - (x - length + 1)],
    'right': lambda x, y, length: [-(y - length + 1), x]
}
LENGTHS = {
    'left': lambda image: len(image[0]),
    'right': lambda image: len(image)
}
RGB_VALUE = 255


def rotate_pixel(direction, x, y, length, image):
    coords = DIRECTIONS[direction](x, y, length)
    return image[coords[0]][coords[1]]


def rotate(image, direction):
    length_row = len(image)
    length_col = len(image[0])
    length = LENGTHS[direction](image)

    rotated = [[rotate_pixel(direction, x, y, length, image)
                for y in range(length_row)] for x in range(length_col)]
    return rotated


def rotate_left(image):
    return rotate(image, 'left')


def rotate_right(image):
    return rotate(image, 'right')


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


def invert(image):
    return change_pixels(image, invert_pixel)


def lighten(image, coeff):
    return change_pixels(image, lighten_pixel, coeff)


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
