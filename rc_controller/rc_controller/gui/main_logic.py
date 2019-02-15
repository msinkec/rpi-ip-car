from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
from threading import Thread
from .main_gui import Ui_MainWindow
import controls


class MainWindow():
    
    def __init__(self, sock, car_addr, controls_port):
        app = QtWidgets.QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(main_window)

        self.sock = sock
        self.car_addr = car_addr
        self.controls_port = controls_port

        # Set of currently pressed keys
        self.pressed_keys = set()   

        # Handle keys for car control to the main window.
        # We attach the method to the gui object to avoid changing
        # the auto-generated file.
        main_window.keyPressEvent = self.on_key_press
        main_window.keyReleaseEvent = self.on_key_release
        
        # We open a sepperate thread that is checking for pressed keys and
        # then preiodically send UDP packets every n milliseconds.
        key_handler_thread = Thread(target=self.handle_keys)
        key_handler_thread.start()

        main_window.show()
        app.exec_()

    def on_key_press(self, key_event):
        if not key_event.isAutoRepeat():
            key = key_event.key()
            self.pressed_keys.add(key)

    def on_key_release(self, key_event):
        if not key_event.isAutoRepeat():   
            key = key_event.key() 
            self.pressed_keys.discard(key)

    def handle_keys(self):
        while True:
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
            print(commands)
            controls.execute(commands, self.sock, self.car_addr, self.controls_port)
        

