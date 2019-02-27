import subprocess as sp
import os
import cv2
import numpy as np
import threading
import socket
import struct
import io
from PIL import Image

def play_feed(video_port): 
    # mplayer is currently used to play back the video feed.
    # TODO: Implement way to play back the stream in the QT app itself.
    #netcat = subprocess.Popen(('nc', '-l', '-p', str(video_port)), stdout=subprocess.PIPE)
    #mplayer = subprocess.Popen(('mplayer', '-noconsolecontrols', '-nolirc' , '-fps', '60',
    #              '-cache', '1024', '-'), stdin=netcat.stdout)


    thr = threading.Thread(target = test, args = (video_port, ))
    thr.start()
 
    return []


def test(video_port):
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', video_port))
    server_socket.listen(1)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        while True:
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
            image = Image.open(image_stream)

            data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
            imagedisp = cv2.imdecode(data, 1)

            cv2.imshow("Frame",imagedisp)
    finally:
        connection.close()
        server_socket.close()
