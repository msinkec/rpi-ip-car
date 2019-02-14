from PyQt5 import QtCore, QtGui, QtWidgets
import sys
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
        main_window.keyPressEvent = self.key_press_handler
        main_window.keyReleaseEvent = self.key_release_handler        

        main_window.show()
        app.exec_()

    def key_press_handler(self, key_event):
        # If the key is being held down, this method gets auto-repeated.
        # This is by design. We want to keep sending UDP packets to the car
        # because it doesn't keep a state about the keys for now.
        key = key_event.key()
        self.pressed_keys.add(key)

        self.handle_keys()

    def key_release_handler(self, key_event):
        if not key_event.isAutoRepeat():   
            key = key_event.key() 
            self.pressed_keys.discard(key)

    def handle_keys(self):
        # Translate keys into commands and hand them over to the control pacakge.
        commands = set()
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
        controls.execute(commands, self.sock, self.car_addr, self.controls_port)

        

