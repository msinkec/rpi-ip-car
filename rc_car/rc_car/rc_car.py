import signal
import sys
import socket
import optparse
import video
import controls
import time
import hashlib

class Main:

    def signal_handler(self, signal, frame):
        self.finish();

    def finish(self):
        self.clear_session()
        self.sock.close()
        sys.exit(0);

    def authenticate(password):
        # Currently only password SHA-512 hash of the car is checked.
        # TODO: Save hash in some configuration file. (The hardcoded one is of the string "default")
        pass_hash = hashlib.sha512(password).hexdigest()
        if pass_hash == 'c46f6204075636e89e9241c32ec6e03d04884d08d5aa52abaf3b0bb8eb74d60a24145c7fd9f97f5fd0300a602e575a9a689b95cd68ce3eccc8b6a4aea1975db8':
            return True
        return False

    def clear_session(self): 
        self.controller_addr = None
        # Clean up subprocesses.
        for subprocess in self.subprocesses:
            subprocess.kill()

    def __init__(self):
        # List of subprocesses
        self.subprocesses = []
        
        # The IP-address of the controller
        self.controller_addr = None

        # Parse command input.
        parser = optparse.OptionParser(usage='OPTIONS:\n' +  
                                        '--videoport <video port> --controlport <controls port>')
        parser.add_option('--videoport', dest='video_port', type='int', default=16168)
        parser.add_option('--controlport', dest='controls_port', type='int', default=16169)

        (options, args) = parser.parse_args()
        
        video_port = options.video_port
        controls_port = options.controls_port

        # Set up handler for SIGINT signals.
        signal.signal(signal.SIGINT, self.signal_handler)

        # Execute initial authentication.
        # TODO: Communication is in CLEARTEXT. Change to TLS or something.
        host = '127.0.0.1'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, controls_port))
        print('Waiting for controller...')
        
        while True:
            msg, addr = self.sock.recvfrom(1024)
            
            if msg.startswith('LOGON') and authenticate(msg.split()[1]):
                # If authentication was successfull, switch to new controller.
                self.clear_session()     # Clear stuff from previous session
                self.controller_addr = addr
                self.subprocesses += video.initialize_feed(self.controller_addr, video_port)
                # Send an approval response to the controller
                self.sock.sendto(controller_addr, 'CONNECTED')
                print("Controller connected!: " + self.controller_addr)
            
            if addr==self.controller_addr:
                # Check for special commands.
                if msg == 'LOGOFF':
                    self.clear_session()
                elif msg == 'SHUTDOWN':
                    pass
                else:
                    # If msg is none of the above, then it's a control command.
                    # If it's malformed, it gets discarded.
                    controls.execute(msg)


if __name__ == '__main__':
    Main()

