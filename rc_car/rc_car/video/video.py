import subprocess
import threading
import io
import socket
import struct
import cv2
import picamera
import time
import numpy as np


class VideoStreamer:
    
    def __init__(self, remote_addr, video_port):
        self.remote_addr = remote_addr
        self.video_port = video_port
        self.subprocesses = []

    def start(self):
        # Using a simpler method with raspivid and netcat for a low latency stream
        # Sends video in H264 format
        raspivid = subprocess.Popen(('raspivid', '-w', '640', '-h', '480',
            '--nopreview', '-o', '-', '-t', '0'), 
                                       stdout=subprocess.PIPE)
        netcat = subprocess.Popen(('nc', self.remote_addr, str(self.video_port)), 
                stdin=raspivid.stdout)
        self.subprocesses.append(raspivid)
        self.subprocesses.append(netcat)


    def finish(self):
        for subprocess in self.subprocesses:
            subprocess.kill();

