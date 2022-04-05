
# 显示图片函数
from PIL import Image


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