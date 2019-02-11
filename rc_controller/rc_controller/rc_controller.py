import optparse
import video
from threading import Thread


def main():
    # TODO: Parse command input
    parser = optparse.OptionParser(usage='Usage %prog --videoport <video port> --controlport <controls port>')

    parser.add_option('--videoport', dest='video_port', type='int', default=16168)
    parser.add_option('--controlport', dest='controls_port', type='int', default=16169)

    (options, args) = parser.parse_args()
    
    video_port = options.video_port
    controls_port = options.controls_port

    # TODO: Wait for car to get online
    

    # TODO: Start to display video feed in a seperate thread
    video_thread = Thread(target = video.play_feed, args = (video_port, ))
    video_thread.start()

    # TODO: Open up a QT window for car controlling


if __name__ == '__main__':
    main()
