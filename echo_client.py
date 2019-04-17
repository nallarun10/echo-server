import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    """ instantiate a TCP socket with IPv4 Addressing, call the socket you make 'sock'"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    """connect your socket to the server here"""
    sock.connect(server_address)

    """ variable to accumulate the entire message received back
    from the server"""
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket

    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(msg.encode('utf-8'))
        """send your message to the server here"""
        while True:
            """Server should be sending you back your message as a series
               of 16-byte chunks. Accumulate the chunks you get to build the
               entire reply from the server. Make sure that you have received
               the entire message and then you can break the loop.
               Log each chunk you receive.  Use the print statement helpful in debugging problems"""
            chuck = sock.recv(16)
            received_message += chuck.decode('utf8')
            print('received "{0}"'.format(chuck.decode('utf8')), file=log_buffer)
            if len(chuck) < 16:
                print (f'Data receving is complete or no data recevied')
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        """ break out of the loop receiving echoed chunks from
        the server you will want to close your client socket."""
        print('closing socket', file=log_buffer)
        sock.close()
        """ Return the entire replymessage received from the server as the return value of this function"""
    return received_message

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
