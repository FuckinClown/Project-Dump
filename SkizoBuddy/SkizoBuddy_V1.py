import pyautogui
import random
import time
import sys
import pyscreeze
import tempfile
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.rectangles = []  # List to store rectangles and texts
        self.screen_width, self.screen_height = pyautogui.size()
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.timer = QTimer(self)  # Timer for the capture and draw functionality
        self.timer.timeout.connect(self.capture_and_draw)
        self.timer.start(50)  # Start the timer
        self.restart_timer = QTimer(self)  # Timer to restart the capture process
        self.restart_timer.timeout.connect(self.restart_capture)
        self.target_region = None
        self.tracking_start_time = None
        print("Overlay window initialized")

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
        global temp_filename
        if self.target_region is None:
            print("Capturing random square...")
            x = random.randint(0, self.screen_width - 100)
            y = random.randint(0, self.screen_height - 100)
            self.target_region = (x, y, 100, 100)
            screenshot = pyautogui.screenshot(region=self.target_region)
            temp_filename = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
            screenshot.save(temp_filename)
            print(f"Target square: ({x}, {y})")
            time.sleep(3)
            print('-'*45)
            self.tracking_start_time = time.time()
        else:
            if time.time() - self.tracking_start_time <= 10:
                try:
                    self.remove_all_rectangles()  # Remove old rectangles
                    for item in pyautogui.locateAllOnScreen(temp_filename, confidence=0.5, limit=1):
                        x, y, width, height = item.left, item.top, item.width, item.height
                        self.add_rectangle(x, y, width, height, "Holy shit im tweakin nigga")
                except pyscreeze.ImageNotFoundException:
                    print("No items found in screenshot")
                    self.remove_all_rectangles()
                    self.timer.stop()  # Stop the current timer
                    print("Waiting 10 seconds...")
                    self.restart_timer.start(10000)  # Wait 60 seconds before restarting
            else:
                print("Tracking completed")
                self.remove_all_rectangles()
                self.timer.stop()  # Stop the current timer
                print("Waiting 10 seconds...")
                self.restart_timer.start(10000)  # Wait 60 seconds before restarting

    def restart_capture(self):
        self.restart_timer.stop()  # Stop the restart timer
        self.target_region = None  # Reset the target region
        self.timer.start(50)  # Restart the capture and draw process

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    print("Overlay window displayed")
    sys.exit(app.exec_())