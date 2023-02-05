from win32gui import *
from win32con import *
import numpy as np
import win32ui
import cv2


class ScreenCapturer:
    def __init__(self, name):
        self.handle = FindWindow(None, name)
        rect = GetWindowRect(self.handle)
        self.left, self.top, _, _ = rect
        _, _, self.right, self.bottom = rect
        self.width = self.right - self.left
        self.height = self.bottom - self.top


    def grab_screen(self):
        hwndDC = GetWindowDC(self.handle)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.width, self.height)

        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (self.width, self.height), mfcDC, (0, 0), SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        picture = np.frombuffer(bmpstr, dtype='uint8')
        picture.shape = (self.height, self.width, 4)

        mfcDC.DeleteDC()
        saveDC.DeleteDC()
        ReleaseDC(self.handle, hwndDC)
        DeleteObject(saveBitMap.GetHandle())

        return picture


    def save_screen(self, path):
        picture = self.grab_screen()
        cv2.imwrite(path, cv2.cvtColor(picture, cv2.COLOR_RGBA2RGB))
