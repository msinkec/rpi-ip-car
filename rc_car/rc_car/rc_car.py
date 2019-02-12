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

    def authenticate(self, password):
        # Currently only password SHA-512 hash of the car is checked.
        # TODO: Save hash in some configuration file. (The hardcoded one is of the string "default")
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        if pass_hash == hashlib.sha512('default'.encode()).hexdigest(): 
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', controls_port))
        print('Waiting for controller...')
        
        while True:
            msg, addr = self.sock.recvfrom(1024)
            msg = msg.decode()

            print("Got msg: " + msg)
            
            if msg.startswith('LOGON') and self.authenticate(msg.split()[1]):
                # If authentication was successfull, switch to new controller.
                self.clear_session()     # Clear stuff from previous session
                self.controller_addr = addr[0]
                self.subprocesses += video.initialize_feed(self.controller_addr, video_port)
                # Send an approval response to the controller
                self.sock.sendto('CONNECTED'.encode(), (self.controller_addr, controls_port))
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

