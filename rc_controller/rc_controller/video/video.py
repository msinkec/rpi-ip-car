import subprocess
import os

def play_feed(video_port):
    """
    # Start a socket listening for connections on 0.0.0.0:<video port> (0.0.0.0 means
    # all interfaces)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', video_port))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        while True:
            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)

            file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cv2.imshow('Video feed', img)
            cv2.waitKey(1)       

    finally:
        connection.close()
        server_socket.close()
    """
    
    # mplayer is currently used to play back the video feed.
    # TODO: Implement way to play back the stream in the QT app itself.
    netcat = subprocess.Popen(('nc', '-l', '-p', str(video_port)), stdout=subprocess.PIPE)
    with open(os.devnull, 'wb') as devnull:
        mplayer = subprocess.Popen(('mplayer', '-noconsolecontrols' , '-fps', '60',
                  '-cache', '1024', '-'), stdin=netcat.stdout, stdout=devnull)
    
    return [netcat, mplayer]
