import socket
import optparse
import video
import signal
import sys
import time


class Main:
    
    def signal_handler(self, signal, frame):
        self.finish();

    def finish(self):
        self.sock.close()
        # Clean up subprocesses
        for subprocess in self.subprocesses:
            subprocess.kill()
        sys.exit(0)

    def __init__(self):
        # List of subprocesses
        self.subprocesses = []
        
        # TODO: Parse command input
        parser = optparse.OptionParser(usage='Usage %prog -a <car IP>\n -p <car PASSWORD>' +  
                                    'Optional:\n --videoport <video port> --controlport <controls port>')
        parser.add_option('-a', dest='car_addr', type='string')
        parser.add_option('-p', dest='car_pass', type='string')
        #parser.add_option('--videoport', dest='video_port', type='int', default=16168)
        #parser.add_option('--controlport', dest='controls_port', type='int', default=16169)
        parser.add_option('--videoport', dest='video_port', type='int', default=16168)
        parser.add_option('--controlport', dest='controls_port', type='int', default=5000)
        
        (options, args) = parser.parse_args()
        if options.car_addr is None:
            print(parser.usage)
            exit(1)
        
        car_addr = options.car_addr
        car_pass = options.car_pass
        video_port = options.video_port
        controls_port = options.controls_port

        # Set up handler for SIGINT signals
        signal.signal(signal.SIGINT, self.signal_handler)

        # Establish connection.
        #host = '127.0.0.1'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', controls_port))

        # Send LOGON request along with entered password to the car.
        msg = 'LOGON ' + car_pass
        self.sock.sendto(msg.encode(), (car_addr, controls_port))

        # Wait for approval.
        self.sock.settimeout(10)
        print("Waiting for car to respond...")
        msg, addr = self.sock.recvfrom(1024)
        if msg == 'CONNECTED':
            self.sock.settimeout(None)
            # Start to display video feed
            self.subprocesses += video.play_feed(video_port)
            # TODO: Listen for controls
            while True:
                comm = input("> ")
                self.sock.sendto(comm, (car_addr, controls_port))

        self.finish()


if __name__ == '__main__':
    Main()
