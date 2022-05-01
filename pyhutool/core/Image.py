import os
import sys
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
def resizeImage(imageName, newImageName = None, size = None):
    if imageName is None:
        raise Exception('imageName is None')
    if os.path.exists(imageName) is False:
        raise Exception('imageName is not exists')
    if size is None or type(size) != tuple:
        raise Exception('size must be tuple')
    if newImageName is None:
        newImageName = imageName
    image = Image.open(imageName)
    im = image.resize(size)
    im.save(newImageName)
    image.close()
    return True


def hex2rgb(hex):
    """
    十六进制颜色转RGB
    :param hex: 十六进制颜色
    :return: RGB颜色
    """
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))


def rgb2hex(rgb):
    """
    RGB转16进制颜色
    :param rgb: RGB颜色
    :return: 16进制颜色
    """
    return '#%02x%02x%02x' % rgb


def replaceColor(imageName, originColor, newColor):
    """
    图片颜色替换函数
    :param imageName: 图片
    :param originalColor: 原始颜色
    :param newColor: 新颜色
    :return:
    """
    if imageName is None:
        raise Exception('imageName is None')
    if os.path.exists(imageName) is False:
        raise Exception('imageName is not exists')
    if isinstance(originColor, str):
        originColor = hex2rgb(originColor)
    if isinstance(newColor, str):
        newColor = hex2rgb(newColor)
    im = Image.open(imageName)
    image = im.convert('RGB')
    imagePixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if imagePixels[x, y] == originColor:
                imagePixels[x, y] = newColor
    image.save(imageName)
    image.close()
    im.close()


# 图片水印函数
def watermarkImage(imageName, watermarkName, x, y):
    if imageName is None or watermarkName is None:
        raise Exception('imageName or watermarkName is None')
    if os.path.exists(imageName) is False or os.path.exists(watermarkName) is False:
        raise Exception('imageName or watermarkName is not exists')
    image = Image.open(imageName)
    watermark = Image.open(watermarkName)
    image.paste(watermark, (x, y))
    image.save(imageName)
    image.close()
    watermark.close()


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


# 识别图片中的人脸函数
def face_detect(imageName):
    im = cv2.imread(imageName)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

