import collections
import datetime
import os
import subprocess
import sys
import functools
import time
import win32api
import win32con
import win32gui
import win32ui
from PIL import ImageGrab
from pyhutool.gui.Const import _const

try:
    from PIL import Image
    from PIL import ImageOps
    from PIL import ImageDraw

    if sys.platform == 'win32':  # TODO - Pillow now supports ImageGrab on macOS.
        from PIL import ImageGrab
    _PILLOW_UNAVAILABLE = False
except ImportError:
    _PILLOW_UNAVAILABLE = True

scrotExists = False
try:
    if sys.platform not in ('java', 'darwin', 'win32'):
        whichProc = subprocess.Popen(
            ['which', 'scrot'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        scrotExists = whichProc.wait() == 0
except OSError as ex:
    # if ex.errno == errno.ENOENT:
    # if there is no "which" program to find scrot, then assume there
    # is no scrot.
    # pass
    # else:
    #     raise
    raise

try:
    import cv2, numpy

    useOpenCV = True
    RUNNING_CV_2 = cv2.__version__[0] < '3'
except ImportError:
    useOpenCV = False


def requiresPillow(wrappedFunction):
    @functools.wraps(wrappedFunction)
    def wrapper(*args, **kwargs):
        if _PILLOW_UNAVAILABLE:
            raise Exception('The Pillow package is required to use this function.')
        return wrappedFunction(*args, **kwargs)

    return wrapper


def _screenshot_win32(imageFilename=None, region=None):
    im = ImageGrab.grab()
    if region is not None:
        assert len(region) == 4, 'region argument must be a tuple of four ints'
        region = [int(x) for x in region]
        im = im.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))
    if imageFilename is not None:
        im.save(imageFilename)
    return im


def _screenshot_osx(imageFilename=None, region=None):
    if imageFilename is None:
        tmpFilename = 'screenshot%s.png' % (datetime.datetime.now().strftime('%Y-%m%d_%H-%M-%S-%f'))
    else:
        tmpFilename = imageFilename
    subprocess.call(['screencapture', '-x', tmpFilename])
    im = Image.open(tmpFilename)

    if region is not None:
        assert len(region) == 4, 'region argument must be a tuple of four ints'
        region = [int(x) for x in region]
        im = im.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))
        os.unlink(tmpFilename)  # delete image of entire screen to save cropped version
        im.save(tmpFilename)
    else:
        # force loading before unlinking, Image.open() is lazy
        im.load()

    if imageFilename is None:
        os.unlink(tmpFilename)
    return im


def _screenshot_linux(scrotExists=False, imageFilename=None, region=None):
    if not scrotExists:
        raise NotImplementedError('"scrot" must be installed to use screenshot functions in Linux. Run: sudo apt-get install scrot')
    if imageFilename is None:
        tmpFilename = '.screenshot%s.png' % (datetime.datetime.now().strftime('%Y-%m%d_%H-%M-%S-%f'))
    else:
        tmpFilename = imageFilename
    if scrotExists:
        subprocess.call(['scrot', '-z', tmpFilename])
        im = Image.open(tmpFilename)
        if region is not None:
            assert len(region) == 4, 'region argument must be a tuple of four ints'
            region = [int(x) for x in region]
            im = im.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))
            os.unlink(tmpFilename)  # delete image of entire screen to save cropped version
            im.save(tmpFilename)
        else:
            # force loading before unlinking, Image.open() is lazy
            im.load()

        if imageFilename is None:
            os.unlink(tmpFilename)
        return im
    else:
        raise Exception('The scrot program must be installed to take a screenshot with PyScreeze on Linux. Run: sudo apt-get install scrot')


RUNNING_PYTHON_2 = sys.version_info[0] == 2
if useOpenCV:
    if RUNNING_CV_2:
        LOAD_COLOR = cv2.CV_LOAD_IMAGE_COLOR
        LOAD_GRAYSCALE = cv2.CV_LOAD_IMAGE_GRAYSCALE
    else:
        LOAD_COLOR = cv2.IMREAD_COLOR
        LOAD_GRAYSCALE = cv2.IMREAD_GRAYSCALE

if not RUNNING_PYTHON_2:
    unicode = str  # On Python 3, all the isinstance(spam, (str, unicode)) calls will work the same as Python 2.

Box = collections.namedtuple('Box', 'left top width height')
Point = collections.namedtuple('Point', 'x y')
RGB = collections.namedtuple('RGB', 'red green blue')

if sys.platform.startswith('java'):
    raise NotImplementedError('Jython is not yet supported by PyScreeze.')
elif sys.platform == 'darwin':
    screenshot = _screenshot_osx
elif sys.platform == 'win32':
    screenshot = _screenshot_win32
else:
    screenshot = _screenshot_linux


def _locateAll_opencv(needleImage, haystackImage, grayscale=None, limit=10000, region=None, step=1,
                      confidence=0.999):
    """
    TODO - rewrite this
        faster but more memory-intensive than pure python
        step 2 skips every other row and column = ~3x faster but prone to miss;
            to compensate, the algorithm automatically reduces the confidence
            threshold by 5% (which helps but will not avoid all misses).
        limitations:
          - OpenCV 3.x & python 3.x not tested
          - RGBA images are treated as RBG (ignores alpha channel)
    """
    if grayscale is None:
        grayscale = _const.GRAYSCALE_DEFAULT

    confidence = float(confidence)

    needleImage = _load_cv2(needleImage, grayscale)
    needleHeight, needleWidth = needleImage.shape[:2]
    haystackImage = _load_cv2(haystackImage, grayscale)

    if region:
        haystackImage = haystackImage[region[1]:region[1] + region[3],
                        region[0]:region[0] + region[2]]
    else:
        region = (0, 0)  # full image; these values used in the yield statement
    if (haystackImage.shape[0] < needleImage.shape[0] or
            haystackImage.shape[1] < needleImage.shape[1]):
        # avoid semi-cryptic OpenCV error below if bad size
        raise ValueError('needle dimension(s) exceed the haystack image or region dimensions')

    if step == 2:
        confidence *= 0.95
        needleImage = needleImage[::step, ::step]
        haystackImage = haystackImage[::step, ::step]
    else:
        step = 1

    # get all matches at once, credit: https://stackoverflow.com/questions/7670112/finding-a-subimage-inside-a-numpy-image/9253805#9253805
    result = cv2.matchTemplate(haystackImage, needleImage, cv2.TM_CCOEFF_NORMED)
    match_indices = numpy.arange(result.size)[(result > confidence).flatten()]
    matches = numpy.unravel_index(match_indices[:limit], result.shape)

    if len(matches[0]) == 0:
        if _const.USE_IMAGE_NOT_FOUND_EXCEPTION:
            raise Exception('Could not locate the image (highest confidence = %.3f)' % result.max())
        else:
            return

    # use a generator for API consistency:
    matchx = matches[1] * step + region[0]  # vectorized
    matchy = matches[0] * step + region[1]
    for x, y in zip(matchx, matchy):
        yield Box(x, y, needleWidth, needleHeight)


def _load_cv2(img, grayscale=None):
    if grayscale is None:
        grayscale = _const.GRAYSCALE_DEFAULT
    if isinstance(img, (str, unicode)):
        if grayscale:
            img_cv = cv2.imread(img, LOAD_GRAYSCALE)
        else:
            img_cv = cv2.imread(img, LOAD_COLOR)
        if img_cv is None:
            raise IOError("Failed to read %s because file is missing, "
                          "has improper permissions, or is an "
                          "unsupported or invalid format" % img)
    elif isinstance(img, numpy.ndarray):
        if grayscale and len(img.shape) == 3:  # and img.shape[2] == 3:
            img_cv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_cv = img
    elif hasattr(img, 'convert'):
        img_array = numpy.array(img.convert('RGB'))
        img_cv = img_array[:, :, ::-1].copy()  # -1 does RGB -> BGR
        if grayscale:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    else:
        raise TypeError('expected an image filename, OpenCV numpy array, or PIL image')
    return img_cv


def locate(needleImage, haystackImage, **kwargs):
    kwargs['limit'] = 1
    points = tuple(locateAll(needleImage, haystackImage, **kwargs))
    if len(points) > 0:
        return points[0]
    else:
        if _const.USE_IMAGE_NOT_FOUND_EXCEPTION:
            raise Exception('Could not locate the image.')
        else:
            return None


def locateOnScreen(image, minSearchTime=0, **kwargs):
    """TODO - rewrite this
    minSearchTime - amount of time in seconds to repeat taking
    screenshots and trying to locate a match.  The default of 0 performs
    a single search.
    """
    start = time.time()
    while True:
        try:
            screenshotIm = screenshot(
                region=None)  # the locateAll() function must handle cropping to return accurate coordinates, so don't pass a region here.
            retVal = locate(image, screenshotIm, **kwargs)
            try:
                screenshotIm.fp.close()
            except AttributeError:
                # Screenshots on Windows won't have an fp since they came from
                # ImageGrab, not a file. Screenshots on Linux will have fp set
                # to None since the file has been unlinked
                pass
            if retVal or time.time() - start > minSearchTime:
                return retVal
        except:
            if time.time() - start > minSearchTime:
                if _const.USE_IMAGE_NOT_FOUND_EXCEPTION:
                    raise
                else:
                    return None


def _kmp(needle, haystack, _dummy):
    shifts = [1] * (len(needle) + 1)
    shift = 1
    for pos in range(len(needle)):
        while shift <= pos and needle[pos] != needle[pos - shift]:
            shift += shifts[pos - shift]
        shifts[pos + 1] = shift
    startPos = 0
    matchLen = 0
    for c in haystack:
        while matchLen == len(needle) or \
                matchLen >= 0 and needle[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(needle):
            yield startPos


def _steppingFind(needle, haystack, step):
    """
    TODO
    """
    for startPos in range(0, len(haystack) - len(needle) + 1):
        foundMatch = True
        for pos in range(0, len(needle), step):
            if haystack[startPos + pos] != needle[pos]:
                foundMatch = False
                break
        if foundMatch:
            yield startPos


@requiresPillow
def _locateAll_python(needleImage, haystackImage, grayscale=None, limit=None, region=None, step=1, confidence=None):
    """
    TODO
    """
    if confidence is not None:
        raise NotImplementedError('The confidence keyword argument is only available if OpenCV is installed.')

    # setup all the arguments
    if grayscale is None:
        grayscale = _const.GRAYSCALE_DEFAULT

    needleFileObj = None
    if isinstance(needleImage, (str, unicode)):
        # 'image' is a filename, load the Image object
        needleFileObj = open(needleImage, 'rb')
        needleImage = Image.open(needleFileObj)

    haystackFileObj = None
    if isinstance(haystackImage, (str, unicode)):
        # 'image' is a filename, load the Image object
        haystackFileObj = open(haystackImage, 'rb')
        haystackImage = Image.open(haystackFileObj)

    if region is not None:
        haystackImage = haystackImage.crop((region[0], region[1], region[0] + region[2], region[1] + region[3]))
    else:
        region = (0, 0)  # set to 0 because the code always accounts for a region

    if grayscale:  # if grayscale mode is on, convert the needle and haystack images to grayscale
        needleImage = ImageOps.grayscale(needleImage)
        haystackImage = ImageOps.grayscale(haystackImage)
    else:
        # if not using grayscale, make sure we are comparing RGB images, not RGBA images.
        if needleImage.mode == 'RGBA':
            needleImage = needleImage.convert('RGB')
        if haystackImage.mode == 'RGBA':
            haystackImage = haystackImage.convert('RGB')

    # setup some constants we'll be using in this function
    needleWidth, needleHeight = needleImage.size
    haystackWidth, haystackHeight = haystackImage.size

    needleImageData = tuple(needleImage.getdata())
    haystackImageData = tuple(haystackImage.getdata())

    needleImageRows = [needleImageData[y * needleWidth:(y + 1) * needleWidth] for y in range(needleHeight)]  # LEFT OFF - check this
    needleImageFirstRow = needleImageRows[0]

    assert len(
        needleImageFirstRow) == needleWidth, 'For some reason, the calculated width of first row of the needle image is not the same as the width of the image.'
    assert [len(row) for row in needleImageRows] == [
        needleWidth] * needleHeight, 'For some reason, the needleImageRows aren\'t the same size as the original image.'

    numMatchesFound = 0

    # NOTE: After running tests/benchmarks.py on the following code, it seem that having a step
    # value greater than 1 does not give *any* significant performance improvements.
    # Since using a step higher than 1 makes for less accurate matches, it will be
    # set to 1.
    step = 1  # hard-code step as 1 until a way to improve it can be figured out.

    if step == 1:
        firstFindFunc = _kmp
    else:
        firstFindFunc = _steppingFind

    for y in range(haystackHeight):  # start at the leftmost column
        for matchx in firstFindFunc(needleImageFirstRow, haystackImageData[y * haystackWidth:(y + 1) * haystackWidth], step):
            foundMatch = True
            for searchy in range(1, needleHeight, step):
                haystackStart = (searchy + y) * haystackWidth + matchx
                if needleImageData[searchy * needleWidth:(searchy + 1) * needleWidth] != haystackImageData[
                                                                                         haystackStart:haystackStart + needleWidth]:
                    foundMatch = False
                    break
            if foundMatch:
                # Match found, report the x, y, width, height of where the matching region is in haystack.
                numMatchesFound += 1
                yield Box(matchx + region[0], y + region[1], needleWidth, needleHeight)
                if limit is not None and numMatchesFound >= limit:
                    # Limit has been reached. Close file handles.
                    if needleFileObj is not None:
                        needleFileObj.close()
                    if haystackFileObj is not None:
                        haystackFileObj.close()
                    return

    # There was no limit or the limit wasn't reached, but close the file handles anyway.
    if needleFileObj is not None:
        needleFileObj.close()
    if haystackFileObj is not None:
        haystackFileObj.close()

    if numMatchesFound == 0:
        if _const.USE_IMAGE_NOT_FOUND_EXCEPTION:
            raise Exception('Could not locate the image.')
        else:
            return


def checkRect(rect):
    try:
        left, top, right, bottom = rect
    except ValueError:
        raise ValueError("%r is not a valid rect; must contain 4 ints" % (rect,))
    if not all(isinstance(x, (int, int)) for x in rect):
        raise ValueError("%r is not a valid rect; must contain 4 ints" % (rect,))
    width = right - left
    height = bottom - top
    if width <= 0 or height <= 0:
        raise ValueError("%r is not a valid rect; width and height must not be "
                         "zero or negative" % (rect,))


def getDisplayRects():
    HANDLE_MONITOR, HDC_MONITOR, SCREEN_RECT = range(3)
    tries = 150
    lastRects = None
    for _ in range(tries):
        try:
            monitors = win32api.EnumDisplayMonitors(None, None)
        except SystemError:
            lastRects = None
        else:
            for m in monitors:
                m[HDC_MONITOR].Close()
            rects = list(m[SCREEN_RECT] for m in monitors)
            try:
                for rect in rects:
                    checkRect(rect)
            except ValueError:
                lastRects = None
            else:
                if rects == lastRects:
                    return rects
                else:
                    lastRects = rects

    raise Exception("Could not get stable rect information after %d tries; "
                    "last was %r." % (tries, lastRects))


def deleteDCAndBitMap(dc, bitmap):
    dc.DeleteDC()
    handle = bitmap.GetHandle()
    # Trying to DeleteObject(0) will throw an exception; it can be 0 in the case
    # of an untouched win32ui.CreateBitmap()
    if handle != 0:
        win32gui.DeleteObject(handle)


def getVirtualScreenRect():
    tries = 150
    lastRect = None
    for _ in range(tries):
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)

        right = left + width
        bottom = top + height

        rect = (left, top, right, bottom)
        try:
            checkRect(rect)
        except ValueError:
            lastRect = None
        else:
            if rect == lastRect:
                return rect
            else:
                lastRect = rect

    raise Exception("Could not get stable rect information after %d tries; "
                    "last was %r." % (tries, lastRect))


def getDCAndBitMap(saveBmpFilename=None, rect=None):
    if rect is None:
        try:
            rect = getVirtualScreenRect()
        except Exception as e:
            raise Exception("Error during getVirtualScreenRect: " + str(e))
    # rect is already checked
    else:
        checkRect(rect)

    left, top, right, bottom = rect
    width = right - left
    height = bottom - top

    hwndDesktop = win32gui.GetDesktopWindow()

    # Retrieve the device context (DC) for the entire virtual screen.
    hwndDevice = win32gui.GetWindowDC(hwndDesktop)
    ##print("device", hwndDevice)
    assert isinstance(hwndDevice, (int, int)), hwndDevice

    mfcDC = win32ui.CreateDCFromHandle(hwndDevice)
    try:
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        # Above line is assumed to never raise an exception.
        try:
            try:
                saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            except (win32ui.error, OverflowError) as e:
                raise Exception("Could not CreateCompatibleBitmap("
                                "mfcDC, %r, %r) - perhaps too big? Error was: %s" % (width, height, e))
            saveDC.SelectObject(saveBitMap)
            try:
                saveDC.BitBlt((0, 0), (width, height), mfcDC, (left, top), win32con.SRCCOPY)
            except win32ui.error as e:
                raise Exception("Error during BitBlt. "
                                "Possible reasons: locked workstation, no display, "
                                "or an active UAC elevation screen. Error was: " + str(e))
            if saveBmpFilename is not None:
                saveBitMap.SaveBitmapFile(saveDC, saveBmpFilename)
        except:
            deleteDCAndBitMap(saveDC, saveBitMap)
            # Let's just hope the above line doesn't raise an exception
            # (or it will mask the previous exception)
            raise
    finally:
        mfcDC.DeleteDC()

    return saveDC, saveBitMap


if useOpenCV:
    locateAll = _locateAll_opencv
    if not RUNNING_PYTHON_2 and cv2.__version__ < '3':
        locateAll = _locateAll_python
else:
    locateAll = _locateAll_python
