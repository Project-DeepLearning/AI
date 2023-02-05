from ultralytics import YOLO
from Library.WinGraphics import *
from Library.Screenshot import *
from threading import Thread
from PIL import Image
import win32api
import time


class Ultralytics:
    def __init__(self, name):
        self.name = name
        self.model = YOLO("yolov8n.pt")
        self.results = None


    def boxes(self):
        list_boxes = []
        for result in self.results:
            list_boxes += tuple(result.boxes.xyxy.tolist())
        return list_boxes


    def create(self, results):
        for index, box in enumerate(self.results):
            x1, y1, x2, y2 = tuple(self.boxes()[index])
            paint = DrawOnApp(self.name, (255, 0, 0), 1)
            x, y = (x1 + x2) / 2, (y1 + y2) / 2
            win32api.SetCursorPos((int(x), int(y)))
            paint.draw_rectangle(int(x1), int(y1), int(x2), int(y2))
            del paint


    def draws(self):
        while True:
            try:
                screen = ScreenCapturer(self.name)
                image = screen.grab_screen()
                picture = Image.fromarray(image).convert('RGB')
                self.results = self.model.predict(source=picture, device="Cuda:0")
                if self.results:
                    self.create(self.results)
                    break
            except Exception as e:
                print(e)


    def start(self):
        process = Thread(target=self.draws)
        process.start()
