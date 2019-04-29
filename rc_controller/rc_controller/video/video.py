import subprocess as sp
import os
import cv2
import numpy as np
import threading
import socket
import struct
import io

import config
from video.detection import BallDetector


class VideoPlayer:

    def __init__(self, detection):
        self.video_port = config.video_port
        self.detection_switch = detection

        self.subprocesses = []
    
    def start(self):

        if config.netcat_stream == True:
            netcat = sp.Popen(('nc', '-l', '-p', str(self.video_port)), stdout=sp.PIPE)
            mplayer = sp.Popen(('mplayer', '-noconsolecontrols', '-nolirc' , '-fps', '60',
                          '-cache', '1024', '-'), stdin=netcat.stdout)
            self.subprocesses.append(netcat)
            self.subprocesses.append(mplayer)
        else:
            self.finish_stream = False  # This is a flag to get the video thread stop itself

            if self.detection_switch == True:
                self.ball_detector = BallDetector()

            thr = threading.Thread(target = self.initialize_playback)
            thr.start()

    def finish(self):
        self.finish_stream = True
    
        # Clean up subprocesses, if there are any.
        for subprocess in self.subprocesses:
            subprocess.kill()
     
    def initialize_playback(self):
        video_socket = socket.socket()
        video_socket.bind(('0.0.0.0', self.video_port))
        video_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        connection = video_socket.accept()[0].makefile('rb')
        try:
            while True:
                if self.finish_stream:
                    break

                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                # Rewind the stream, open it as an image with opencv and do some
                # processing on it
                image_stream.seek(0)

                data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
                imagedisp = cv2.imdecode(data, 1)

                if self.detection_switch:
                    imagedisp = self.ball_detector.process_frame(imagedisp)

                cv2.imshow("Frame", imagedisp)
        finally:
            connection.close()
            video_socket.close()
