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
        self.detection = detection

        self.subprocesses = []
    
    def start(self):

        if not self.detection:
            netcat = sp.Popen(('nc', '-l', '-p', str(self.video_port)), stdout=sp.PIPE)
            mplayer = sp.Popen(('mplayer', '-noconsolecontrols', '-nolirc' , '-fps', '60',
                          '-cache', '1024', '-'), stdin=netcat.stdout)
            self.subprocesses.append(netcat)
            self.subprocesses.append(mplayer)
        else:
            # This is a flag to get the video thread stop itself
            self.finish_stream = False  
            self.ball_detector = BallDetector()
            thr = threading.Thread(target = self.initialize_playback)
            thr.start()

    def finish(self):
        self.finish_stream = True
    
        # Clean up subprocesses, if there are any.
        for subprocess in self.subprocesses:
            subprocess.kill()
     
    def initialize_playback(self):
        '''
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
                print('okk') 
        finally:
            connection.close()
            video_socket.close()
        '''
        

        netcat = sp.Popen(('nc', '-l', '-p', str(self.video_port)), stdout=sp.PIPE)
        
        command = [ 'ffmpeg',
                '-i', '-',             # fifo is the named pipe
                '-pix_fmt', 'bgr24',      # opencv requires bgr24 pixel format.
                '-vcodec', 'rawvideo',
                '-an','-sn',              # we want to disable audio processing (there is no audio)
                '-f', 'image2pipe', '-']    
        ffmpeg = sp.Popen(command, stdin=netcat.stdout , stdout=sp.PIPE, bufsize=10**4)
        self.subprocesses.append(netcat)
        self.subprocesses.append(ffmpeg)

        while True:
            if self.finish_stream:
                break
            # Capture frame-by-frame
            raw_image = ffmpeg.stdout.read(640*480*3)
            # transform the byte read into a np array
            image =  np.fromstring(raw_image, dtype='uint8')
            # Notice how height is specified first and then width
            image = image.reshape((480,640,3))
            if image is not None:
                image = self.ball_detector.process_frame(image)
                cv2.imshow('Video', image)

            ffmpeg.stdout.flush()

        cv2.destroyAllWindows()

        '''
        netcat = sp.Popen(('nc', '-l', '-p', str(self.video_port)), stdout=sp.PIPE)
        #ffmpegCmd = ['ffmpeg', '-i', '-', '-f', 'rawvideo', '-vcodec', 'bmp', '-vf', 'fps=40', '-']
        #ffmpegCmd = ['ffmpeg', '-i', '-', '-f', 'rawvideo', '-vcodec', 'bmp', '-']
        ffmpegCmd = ['ffmpeg', '-thread_queue_size', '0','-i', '-', '-f', 'rawvideo', '-vcodec', 'bmp',  '-']
        ffmpeg = sp.Popen(ffmpegCmd, stdin = netcat.stdout, stdout = sp.PIPE)
        self.subprocesses.append(netcat)
        self.subprocesses.append(ffmpeg)

        while True:
            fileSizeBytes = ffmpeg.stdout.read(6)

            fileSize = 0
            for i in range(4):
                fileSize += fileSizeBytes[i + 2] * 256 ** i
            bmpData = fileSizeBytes + ffmpeg.stdout.read(fileSize - 6)
            image = cv2.imdecode(np.fromstring(bmpData, dtype = np.uint8), 1)

            cv2.imshow('Frame', image)
        '''
