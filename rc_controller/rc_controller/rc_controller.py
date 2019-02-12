import optparse
import video
import signal
import sys
import time

# List of subprocesses
subprocesses = []


def signal_handler(signal, frame):
    finish();


def finish():
    # Clean up subprocesses
    for subprocess in subprocesses:
        subprocess.kill()
    sys.exit(0)


def main():
    global subprocesses

    # TODO: Parse command input
    parser = optparse.OptionParser(usage='''Usage %prog -a <car IP> 
                            Options:
                            --videoport <video port> --controlport <controls port>''')

    parser.add_option('-a', dest='car_ip', type='string')
    parser.add_option('--videoport', dest='video_port', type='int', default=16168)
    parser.add_option('--controlport', dest='controls_port', type='int', default=16169)

    (options, args) = parser.parse_args()
    if options.car_ip is None:
        print(parser.usage)
        exit(1)
    
    car_ip = options.car_ip
    video_port = options.video_port
    controls_port = options.controls_port

    # Set up handler for SIGINT signals
    signal.signal(signal.SIGINT, signal_handler)

    # TODO: Establish connection. If car IP is unreachable, exit the program.
    

    # TODO: Start to display video feed
    subprocesses += video.play_feed(video_port)
 
    # TODO: Open up a QT window for car controlling

    while True: time.sleep(1)
    finish()

if __name__ == '__main__':
    main()
