from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
from threading import Thread
from .main_gui import Ui_MainWindow
import controls
import config


# TODO: This should be a child of the ui class.
class MainWindow():
    
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(self.main_window)

        # Set of currently pressed keys
        self.pressed_keys = set()

        # This is a flag for child threads to terminate
        self.finish_flag = None

        # Get QObject references
        self.btn_forward = self.main_window.findChild(QtWidgets.QPushButton, "btn_forward")
        self.btn_backward = self.main_window.findChild(QtWidgets.QPushButton, "btn_backward")
        self.btn_left = self.main_window.findChild(QtWidgets.QPushButton, "btn_left")
        self.btn_right = self.main_window.findChild(QtWidgets.QPushButton, "btn_right")

        # Handle keys for car control to the main window.
        # We attach the method to the gui object to avoid changing
        # the auto-generated file.
        self.main_window.keyPressEvent = self.on_key_press
        self.main_window.keyReleaseEvent = self.on_key_release
        
        # We open a sepperate thread that is checking for pressed keys and
        # then preiodically send UDP packets every n milliseconds.
        key_handler_thread = Thread(target=self.handle_keys)
        key_handler_thread.start()

        self.main_window.show()
        self.finish_flag = app.exec_()

    def on_key_press(self, key_event):
        if not key_event.isAutoRepeat():
            key = key_event.key()
            self.pressed_keys.add(key)  # Add key to the pressed set
            self.update_buttons()

    def on_key_release(self, key_event):
        if not key_event.isAutoRepeat():   
            key = key_event.key() 
            self.pressed_keys.discard(key)
            self.update_buttons()

    def update_buttons(self):
        self.btn_forward.setEnabled(False)
        self.btn_backward.setEnabled(False)
        self.btn_left.setEnabled(False)
        self.btn_right.setEnabled(False)
        for key in self.pressed_keys:
            if key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_W:
                self.btn_forward.setEnabled(True)
            elif key == QtCore.Qt.Key_Down or key == QtCore.Qt.Key_S:
                self.btn_backward.setEnabled(True)
            elif key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_D:
                self.btn_right.setEnabled(True)
            elif key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_A:
                self.btn_left.setEnabled(True)

    def handle_keys(self):
        while True:

            # We need some way of knowing when to quit execution of this method.
            if self.finish_flag == 0:
                break

            # Make sure this time period is shorter than:
            # (network latency + command duration on the car).
            # Otherwise the car motors will stutter.
            time.sleep(0.01)

            # Translate keys into commands and hand them over to the control pacakge.
            commands = set()

            if len(self.pressed_keys) == 0:
                continue

            for key in self.pressed_keys:
                if key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_W:
                    commands.add('f')   # Forward
                elif key == QtCore.Qt.Key_Down or key == QtCore.Qt.Key_S:
                    commands.add('b')   # Backwards
                elif key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_D:
                    commands.add('r')   # Steer right 
                elif key == QtCore.Qt.Key_Left or key == QtCore.Qt.Key_A:
                    commands.add('l')   # Steer left 
                elif key == QtCore.Qt.Key_Shift:
                    commands.add('s')   # Speed mode
            controls.execute(commands, config.controls_sock, config.car_addr, config.controls_port)
        

