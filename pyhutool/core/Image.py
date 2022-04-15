from os import PathLike

from PIL import Image
import cv2
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_alt.xml')

def showImage(image, title=None):
    """
    显示图片函数
    :param image: 图片
    :param title: 图片标题
    :return:
    """
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(image)
    plt.axis('off')
    if title is not None:
        plt.title(title)
    plt.show()


# 缩放图片函数
def resizeImage(image, size):
    """
    缩放图片函数
    :param image: 图片
    :param size: 缩放大小
    :return:
    """
    return image.resize(size)

def grayscaleImage(image):
    """
    图片灰度化函数
    :param image: 图片
    :return:
    """
    return image.convert('L')


# 图片二值化函数
def binaryImage(image, threshold=128):
    """
    图片二值化函数
    :param image: 图片
    :param threshold: 阈值
    :return:
    """
    return image.convert('1', dither=Image.FLOYDSTEINBERG, palette=Image.ADAPTIVE, colors=1, threshold=threshold)


# 图片转换为像素点函数
def imageToPixels(image):
    """
    图片转换为像素点函数
    :param image: 图片
    :return:
    """
    return image.load()


def replaceColor(image, original_color, new_color):
    """
    图片颜色替换函数，线性替换
    :param image: 图片
    :param original_color: 原始颜色
    :param new_color: 新颜色
    :return:
    """
    image = image.convert('RGB')
    image_pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if image_pixels[x, y] == original_color:
                image_pixels[x, y] = new_color
    return image


def replaceColorGaussian(image, original_color, new_color):
    """
    图片颜色替换函数，高斯替换
    :param image: 图片
    :param original_color: 原始颜色
    :param new_color: 新颜色
    :return:
    """
    image = image.convert('RGB')
    image_pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if image_pixels[x, y] == original_color:
                image_pixels[x, y] = new_color
    return image


def replaceColorMean(image, original_color, new_color):
    """
    图片颜色替换函数, 均值替换
    :param image: 图片
    :param original_color: 原始颜色
    :param new_color: 新颜色
    :return:
    """
    image = image.convert('RGB')
    image_pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if image_pixels[x, y] == original_color:
                image_pixels[x, y] = new_color
    return image


# 图片水印函数
def watermarkImage(image, watermark, x, y):
    """
    图片水印函数
    :param image: 图片
    :param watermark: 水印图片
    :param x: x坐标
    :param y: y坐标
    :return:
    """
    image.paste(watermark, (x, y))
    return image

# 检测图片类型
def detectImageType(file, h=None):
    f = None
    try:
        if h is None:
            if isinstance(file, (str, PathLike)):
                f = open(file, 'rb')
                h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
        for tf in tests:
            res = tf(h, f)
            if res:
                return res
    finally:
        if f: f.close()
    return None

tests = []

def test_jpeg(h, f):
    """JPEG data in JFIF or Exif format"""
    if h[6:10] in (b'JFIF', b'Exif'):
        return 'jpeg'

tests.append(test_jpeg)

def test_png(h, f):
    if h.startswith(b'\211PNG\r\n\032\n'):
        return 'png'

tests.append(test_png)

def test_gif(h, f):
    """GIF ('87 and '89 variants)"""
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

tests.append(test_gif)

def test_tiff(h, f):
    """TIFF (can be in Motorola or Intel byte order)"""
    if h[:2] in (b'MM', b'II'):
        return 'tiff'

tests.append(test_tiff)

def test_rgb(h, f):
    """SGI image library"""
    if h.startswith(b'\001\332'):
        return 'rgb'

tests.append(test_rgb)

def test_pbm(h, f):
    """PBM (portable bitmap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in b'14' and h[2] in b' \t\n\r':
        return 'pbm'

tests.append(test_pbm)

def test_pgm(h, f):
    """PGM (portable graymap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in b'25' and h[2] in b' \t\n\r':
        return 'pgm'

tests.append(test_pgm)

def test_ppm(h, f):
    """PPM (portable pixmap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in b'36' and h[2] in b' \t\n\r':
        return 'ppm'

tests.append(test_ppm)

def test_rast(h, f):
    """Sun raster file"""
    if h.startswith(b'\x59\xA6\x6A\x95'):
        return 'rast'

tests.append(test_rast)

def test_xbm(h, f):
    """X bitmap (X10 or X11)"""
    if h.startswith(b'#define '):
        return 'xbm'

tests.append(test_xbm)

def test_bmp(h, f):
    if h.startswith(b'BM'):
        return 'bmp'

tests.append(test_bmp)

def test_webp(h, f):
    if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'

tests.append(test_webp)

def test_exr(h, f):
    if h.startswith(b'\x76\x2f\x31\x01'):
        return 'exr'

tests.append(test_exr)

# 检测图片MIME类型
def detectImageMIME(image):
    """
    识别图片MIME类型
    :param image: 图片
    :return:
    """
    return image.mimetype

# 识别图片中的人脸函数
def face_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

