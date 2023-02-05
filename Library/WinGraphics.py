from win32gui import *
from win32api import *
from win32con import *
import math


class DrawOnApp:
    def __init__(self, NAME, COLOR, PIXEL=3):
        self.HWND = FindWindow(None, NAME)
        if not self.HWND:
            raise "Window search failed !"
        self.WDC = GetWindowDC(self.HWND)
        self.PEN = CreatePen(PS_SOLID, PIXEL, RGB(*COLOR))
        self.BRUSH = CreateSolidBrush(RGB(255, 255, 255))


    def draw_line(self, x1, y1, x2, y2):
        SelectObject(self.WDC, self.PEN)
        MoveToEx(self.WDC, x1, y1)
        LineTo(self.WDC, x2, y2)


    def draw_circle(self, x, y, r):
        SelectObject(self.WDC, self.PEN)
        SelectObject(self.WDC, GetStockObject(NULL_BRUSH))
        Ellipse(self.WDC, x - r, y - r, x + r, y + r)


    def draw_rectangle(self, x1, y1, x2, y2):
        SelectObject(self.WDC, self.PEN)
        SelectObject(self.WDC, GetStockObject(NULL_BRUSH))
        Rectangle(self.WDC, x1, y1, x2, y2)


    def draw_ellipse(self, x1, y1, x2, y2):
        SelectObject(self.WDC, self.PEN)
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        a, b = abs((x2 - x1) / 2), abs((y2 - y1) / 2)

        for index in range(361):
            angle = math.radians(index)
            x = int(center_x + a * math.cos(angle))
            y = int(center_y + b * math.sin(angle))
            if index:
                LineTo(self.WDC, x, y)
            else:
                MoveToEx(self.WDC, x, y)


    def __del__(self):
        DeleteObject(self.PEN)
        DeleteObject(self.BRUSH)
        ReleaseDC(self.HWND, self.WDC)

