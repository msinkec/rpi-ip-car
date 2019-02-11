import signal
import sys
import optparse
import video
import time


# List of subprocesses
subprocesses = []


def signal_handler(signal, frame):
    finish();


def finish():
    # TODO: Clean up subprocesses
    for subprocess in subprocesses:
        subprocess.kill()
    sys.exit(0);


def main():
    global subprocesses

    # TODO: Parse command input.
    parser = optparse.OptionParser(usage='Usage: %prog -a <controller address> ' +  
                                    '--videoport <video port> --controlport <controls port>')

    parser.add_option('-a', dest='remote_addr', type='string')
    parser.add_option('--videoport', dest='video_port', type='int', default=16168)
    parser.add_option('--controlport', dest='controls_port', type='int', default=16169)

    (options, args) = parser.parse_args()
    if options.remote_addr is None:
        print(parser.usage)
        exit(1)

    remote_addr = options.remote_addr
    video_port = options.video_port
    controls_port = options.controls_port

    # Set up handler for SIGINT signals
    signal.signal(signal.SIGINT, signal_handler)

    # TODO: Execute initial authentication. (Wait for controller to try to connect to this car and then store the IP.)

    # TODO: Start video streaming. 
    subprocesses += video.initialize_feed(remote_addr, video_port)

    # TODO: Start listening for controls.
    print("Running...")
    while True: time.sleep(1)

    finish()


if __name__ == '__main__':
    main()

