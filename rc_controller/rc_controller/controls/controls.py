# TODO: Special commands.
"""
All commands being sent to the car apply for a fraction of a second.
After that it has to be re-sent.
Commands:
    'f0.3': go forward at 30% speed
    'b0.3': go backwards at 30% speed
    'l': steer left
    'r': steer right
"""

def execute(commands, sock, car_addr, controls_port):
    for comm in commands:
        sock.sendto(comm.encode(), (car_addr, controls_port))

