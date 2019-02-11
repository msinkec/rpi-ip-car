import subprocess

def initialize_feed(remote_addr, video_port):
    """
    # Connect a client socket to <remote_addr>:<video_port>
    client_socket = socket.socket()
    client_socket.connect((remote_addr, video_port))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()
    """

    # Using a simpler method with raspivid and netcat for a low latency stream
    raspivid = subprocess.Popen(('raspivid', '-w', '640', '-h', '480', '--nopreview', '-o', '-', '-t', '0'), 
                                    stdout=subprocess.PIPE)
    netcat = subprocess.Popen(('nc', remote_addr, str(video_port)), stdin=raspivid.stdout)

    return [raspivid, netcat]

