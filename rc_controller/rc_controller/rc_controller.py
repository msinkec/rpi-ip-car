import socket
import optparse
import video
import signal
import sys
import time
import gui

import config


class Main:
    
    def finish(self):
        print("Closing application...")
    
        # Close controls socket
        self.sock.close()

        # Close video stream
        if self.video_player:
            self.video_player.finish()


        sys.exit(0)

    def __init__(self):
        parser = optparse.OptionParser(usage='Usage %prog -a <car IP>\n -p <car PASSWORD>' +  
                                    'Optional:\n --videoport <video port> --controlport <controls port>')
        parser.add_option('-a', dest='car_addr', type='string')
        parser.add_option('-p', dest='car_pass', type='string')
        parser.add_option('--videoport', dest='video_port', type='int', default=16168)
        parser.add_option('--controlport', dest='controls_port', type='int', default=16169)
        parser.add_option('--detection', action='store_true', dest='detection', 
                            default=False, help="Enable object detection.")
        parser.add_option('--netcat', action='store_true', dest='netcat_stream', 
                            default=False, help="Use netcat as video streaming method. Must also be enabled by server (car)")

        (options, args) = parser.parse_args()
        if options.car_addr is None:
            print(parser.usage)
            exit(1)
        
        # Store options to a global static class
        config.car_addr = options.car_addr
        config.car_pass = options.car_pass
        config.video_port = options.video_port
        config.controls_port = options.controls_port
        config.netcat_stream = options.netcat_stream

        detection = options.detection

        # Establish connection.
        #host = '127.0.0.1'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', config.controls_port))

        # Send LOGON request along with entered password to the car.
        msg = 'LOGON ' + config.car_pass
        self.sock.sendto(msg.encode(), (config.car_addr, config.controls_port))

        # Store pointer to the control socket in a static global variable, so it can easily be
        # used elsewhere.
        config.controls_sock = self.sock

        # Wait for approval.
        self.sock.settimeout(10)
        print("Waiting for car to respond...")
        msg, addr = self.sock.recvfrom(1024)
        if msg.decode() == 'CONNECTED':
            print("Connection SUCCESS!")
            self.sock.settimeout(None)
            # Start to listen for video feed
            self.video_player = video.VideoPlayer(detection)
            self.video_player.start()
            # Send confirmation, that the controller is now listening for video connection.
            self.sock.sendto("VIDEO OK".encode(), (config.car_addr, config.controls_port))
            # Open QT window for controlling the car.
            gui.MainWindow()
    
        self.finish()


if __name__ == '__main__':
    Main()
