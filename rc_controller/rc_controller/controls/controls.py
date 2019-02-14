# TODO: Special commands.
"""
All commands being sent to the car apply for a fraction of a second.
After that it has to be re-sent.
Commands:
    'f': go forward
    'b': go backwards
    'l': steer left
    'r': steer right
    's': boost / speed mode
"""

def execute(commands, sock, car_addr, controls_port):
    for comm in commands:
        sock.sendto(comm.encode(), (car_addr, controls_port))

