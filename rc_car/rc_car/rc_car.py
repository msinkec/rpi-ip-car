import signal
import sys
import socket
import optparse
import video
import controls
import time
import hashlib
import controls

class Main:

    def signal_handler(self, signal, frame):
        self.finish();

    def finish(self):
        self.clear_session()
        self.sock.close()
        sys.exit(0);

    def authenticate(self, password):
        # Currently only password SHA-512 hash of the car is checked.
        # TODO: Save hash in some configuration file. (The hardcoded one is of the string "default")
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        if pass_hash == hashlib.sha512('default'.encode()).hexdigest(): 
            return True
        return False

    def clear_session(self):
        self.controller_addr = None
        # Stop video streaming thread.
        if self.video_stream:
            self.video_stream.finish()

    def __init__(self):
        # The IP-address of the controller
        self.controller_addr = None

        self.video_stream = None

        # Parse command input.
        parser = optparse.OptionParser(usage='OPTIONS:\n' +  
                                        '--videoport <video port> --controlport <controls port>')
        parser.add_option('--videoport', dest='video_port', type='int', default=16168)
        parser.add_option('--controlport', dest='controls_port', type='int', default=16169)
        parser.add_option('--netcat', dest='netcat_stream', action='store_true',
                default=False, help='Use netcat method to stream video. Client must also enable this option.')

        (options, args) = parser.parse_args()
        
        video_port = options.video_port
        controls_port = options.controls_port
        netcat_stream = options.netcat_stream

        # Set up handler for SIGINT signals.
        signal.signal(signal.SIGINT, self.signal_handler)

        # Object for executing movement commands.
        car_movement_controls = controls.Movement()

        # Execute initial authentication.
        # TODO: Communication is in CLEARTEXT. Change to TLS or something.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', controls_port))
        print('Waiting for controller...')
        
        self.sock.settimeout(0.1)

        while True: 
            try:
                msg, addr = self.sock.recvfrom(64)
            except socket.timeout:
                # If no packet is received, we still need to update movement
                # to stop moving.
                # This method with the socket timeout is kind of hacky, but it
                # doesn't use sepperate threads and I'm too lazy to do sepperate threads.
                car_movement_controls.update()
                continue

            comm = msg.decode()
 
            if comm.startswith('LOGON') and self.authenticate(comm.split()[1]):
                # If authentication was successfull, switch to new controller.
                self.clear_session()     # Clear stuff from previous session
                self.controller_addr = addr[0]
                # Send an approval response to the controller
                self.sock.sendto('CONNECTED'.encode(), (self.controller_addr, controls_port))
                print("Controller connected!: " + self.controller_addr)
                # Controller must have socket listening for video before we can start streaming.
                msg, addr = self.sock.recvfrom(64)
                if msg.decode() == 'VIDEO OK':
                    print('Controller is listening for video, starting stream.')
                    self.video_stream = video.VideoStreamer(self.controller_addr, video_port)
                    self.video_stream.start(netcat_stream)
                continue
            

            # Check if this packet actually came from the logged on controller.
            if addr[0]==self.controller_addr:
                # Check for special commands.
                if comm == 'LOGOFF':
                    self.clear_session()
                elif comm == 'SHUTDOWN':
                    pass
                else:
                    # If comm is none of the above, then it's a movement command.
                    car_movement_controls.execute(comm)


if __name__ == '__main__':
    Main()

