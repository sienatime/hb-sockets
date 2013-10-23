import socket
import sys
import select

def open_connection(a_socket, host, port):
    a_socket.connect((host, port))

def format_message(message):
    tokens = message.split("::")
    return "[%s] %s" % (tokens[0], tokens[1])

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    open_connection(my_socket, "localhost", 5555)

    data = my_socket.recv(1024)

    print "received:\n%s" %  data

    #get line of input from user using sys.stdin
    # send to server using sendall()

    inp = sys.stdin.readline()
    my_socket.sendall(inp)
    data = my_socket.recv(1024)

    print "received:\n%s" %  data

    running = True
    while running:
        inputready, outputready, exceptready = select.select([my_socket, sys.stdin], [], [])

        for s in inputready:
            if s == sys.stdin:
                msg = s.readline()
                if msg.rstrip() == "/quit":
                    print "Disconnected from server!"
                    running = False
                my_socket.sendall(msg)

            elif s == my_socket:
                if msg:
                    msg = s.recv(1024)
                    if "::" in msg:
                        print format_message(msg)
                    else:
                        print msg
                else:
                    print "Disconnected from server!"
                    running = False

    my_socket.close()

main()