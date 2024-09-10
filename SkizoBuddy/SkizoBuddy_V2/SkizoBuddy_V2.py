import cv2
import numpy as np
import pyautogui
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

detection_body = cv2.CascadeClassifier("detectors\\fullbody.xml")
detection_lowerbod = cv2.CascadeClassifier("detectors\\lowerbody.xml")
detection_upperbod = cv2.CascadeClassifier("detectors\\upperbody.xml")
detection_plate = cv2.CascadeClassifier("detectors\\license_plate.xml")
detection_plate_RU = cv2.CascadeClassifier("detectors\\license_plate_RU.xml")

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.rectangles = [] 
        self.screen_width, self.screen_height = pyautogui.size()
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_and_draw)
        self.timer.start(50)
        self.restart_timer = QTimer(self)
        self.restart_timer.timeout.connect(self.restart_capture)
        self.tracking_start_time = None
        print("Initialization Complete")

    def add_rectangle(self, x, y, width, height, text):
        self.rectangles.append((x, y, width, height, text))
        self.update()  # Update the window to reflect the new rectangle
        print(f"Found item at ({x}, {y})")

    def remove_all_rectangles(self):
        self.rectangles = []  # Clear the list of rectangles
        self.update()  # Update the window to reflect the removal of rectangles

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0))
        painter.setFont(QFont('Arial', 10))
        for rect in self.rectangles:
            x, y, width, height, text = rect
            painter.drawRect(x, y, width, height)
            painter.drawText(x + 10, y + 20, text)

    def capture_and_draw(self):
        if self.tracking_start_time is None:
            self.tracking_start_time = time.time()
        else:
            if time.time() - self.tracking_start_time <= 20: # Tracking time
                screenshot = pyautogui.screenshot()
                screenshot = np.array(screenshot)
                screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

                # Resize ss for better proformance
                resized_width = 800
                aspect_ratio = screenshot_rgb.shape[1] / screenshot_rgb.shape[0]
                resized_height = int(resized_width / aspect_ratio)
                resized_screenshot = cv2.resize(screenshot_rgb, (resized_width, resized_height))
                width_scale = screenshot_rgb.shape[1] / resized_width
                height_scale = screenshot_rgb.shape[0] / resized_height
                screenshot_gray = cv2.cvtColor(resized_screenshot, cv2.COLOR_BGR2GRAY)
                self.remove_all_rectangles()

                det_body = detection_body.detectMultiScale(screenshot_gray, scaleFactor=1.1, minNeighbors=5)
                det_upperbod = detection_upperbod.detectMultiScale(screenshot_gray, scaleFactor=1.1, minNeighbors=5)
                det_lowerbod = detection_lowerbod.detectMultiScale(screenshot_gray, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in det_body:
                    original_x = int(x * width_scale)
                    original_y = int(y * height_scale)
                    original_w = int(w * width_scale)
                    original_h = int(h * height_scale)
                    self.add_rectangle(original_x, original_y, original_w, original_h, "Gods Eyes")
                
                for (x, y, w, h) in det_upperbod:
                    original_x = int(x * width_scale)
                    original_y = int(y * height_scale)
                    original_w = int(w * width_scale)
                    original_h = int(h * height_scale)
                    self.add_rectangle(original_x, original_y, original_w, original_h, "Unsable Code")
                
                for (x, y, w, h) in det_lowerbod:
                    original_x = int(x * width_scale)
                    original_y = int(y * height_scale)
                    original_w = int(w * width_scale)
                    original_h = int(h * height_scale)
                    self.add_rectangle(original_x, original_y, original_w, original_h, "Cosmic Egg")
                
                det_plate1 = detection_plate.detectMultiScale(screenshot_gray, scaleFactor=1.1, minNeighbors=5)
                det_plate2 = detection_plate_RU.detectMultiScale(screenshot_gray, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in det_plate1:
                    original_x = int(x * width_scale)
                    original_y = int(y * height_scale)
                    original_w = int(w * width_scale)
                    original_h = int(h * height_scale)
                    self.add_rectangle(original_x, original_y, original_w, original_h, "Warning Sign")
                
                for (x, y, w, h) in det_plate2:
                    original_x = int(x * width_scale)
                    original_y = int(y * height_scale)
                    original_w = int(w * width_scale)
                    original_h = int(h * height_scale)
                    self.add_rectangle(original_x, original_y, original_w, original_h, "Warning Sign")
                #time.sleep(0.1)
            else:
                print("Tracking completed")
                self.remove_all_rectangles()
                self.timer.stop()
                print("Waiting 30 seconds...")
                self.tracking_start_time = None
                self.restart_timer.start(30000)  # Wait x seconds before restarting
            

    def restart_capture(self):
        self.restart_timer.stop()  # Stop the restart timer
        self.timer.start(50)  # Restart the capture and draw process

if __name__ == "__main__":    
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    print("Overlay window displayed")
    sys.exit(app.exec_())