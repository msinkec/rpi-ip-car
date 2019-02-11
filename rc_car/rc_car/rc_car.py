import optparse
import video
from threading import Thread


def main():
    # TODO: Parse command input.
    parser = optparse.OptionParser(usage='Usage: %prog -a <car address> ' +  
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

    # TODO: Execute initial authentication

    # TODO: Start video streaming thread.
    video_thread = Thread(target = video.initialize_feed, args = (remote_addr, video_port))
    video_thread.start()

    # TODO: Start control listening thread.

if __name__ == '__main__':
    main()

