# The commented is anoter solution - another 'type' of gray
# VALS = [0.2126, 0.7152, 0.0722]


def grayscale(func):
    def decorated_func(*args):
        return make_gray(func(*args))
    return decorated_func


def make_gray_pixel(pix):
    c_lin = int(sum(pix) / 3)
    # c_lin = int(sum([a * b for a, b in zip(VALS, pix)]))
    return (c_lin, c_lin, c_lin)


def make_gray(image):
    return [[make_gray_pixel(image[i][j]) for j
             in range(len(image[0]))] for i in range(len(image))]
