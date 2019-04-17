import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for server
    address = ('127.0.0.1', 10000)

    """instantiate a TCP socket with IPv4 Addressing, 
    calling the socket as 'sock'"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    """ If repeatedly run the server script it fails,
    claiming that the port is already used.  Option to fix this problem. 
    socket library documentation:
    http://docs.python.org/3/library/socket.html#example"""

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
     # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    """ bind 'sock' to the address above and begin to listen
        for incoming connections"""
    sock.bind(address)
    sock.listen(1)
    try:
        """ the outer loop controls the creation of new connection sockets. 
        The server will handle each incoming connection one at a time."""
        while True:
            print('waiting for a connection', file=log_buffer)

            """ make a new socket when a client connects, call it 'conn',
            and get get the address of the client""" 
            try:
                conn, client_address = sock.accept()
                print('connection - {0}:{1}'.format(*client_address), file=log_buffer)

                """ Code to receive messages sent by the client in
                buffers. When a complete message has been received, the
                loop will exit"""
                while True:
                    """ Receive 16 bytes of data from the client. Store
                    the data you receive as 'data'"""
                    data = conn.recv(16)
                    print('received "{0}"'.format(data.decode('utf8')))
                    
                    """ Send the data received back to the client, log
                    the fact using the print statement here : Help in
                    debugging problems"""
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    """Check here to see whether you have received the end
                    of the message. If you have, then break from the `while True`
                    loop"""
                    
                    if len(data) < 16:
                        print ('All data has been sent')
                        break
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                """ When the inner loop exits, the finally' clause will
                close the socket """
                print('echo complete, client connection closed', file=log_buffer)
                conn.close()
                # break
    except KeyboardInterrupt:
        """ Use the python KeyboardInterrupt exception as a signal to
        close the server socket and exit from the server function."""
        # pass
        print('quitting echo server', file=log_buffer)
        sock.close()

if __name__ == '__main__':
    server()
    sys.exit(0)
