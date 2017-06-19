#!/usr/bin/python3

import argparse
import socket
import sys

from pytelnet import Client


def main(telnet):
    try:
        print(telnet.received())
    except socket.timeout:
        pass
    except Exception as e:
        telnet.close()
        sys.exit(e)

    while True:
        request = input('> ')
        if request == '\n':
            continue
        telnet.send(request)

        try:
            while True:
                answer = telnet.received()
                if not answer:
                    sys.exit()
                print(answer)
        except socket.timeout:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, help='The host name or IP address'
                                               ' of the remote computer to '
                                               'which you are connecting.')
    parser.add_argument('port', type=int, help='The port number or '
                                               'service name.')

    args = parser.parse_args()
    telnet = Client()
    try:
        telnet.connect(args.host, args.port)
        main(telnet)
    except KeyboardInterrupt:
        sys.exit("Connection terminated")
    except Exception as e:
        sys.exit('Can not connect to "{}"'.format(sys.argv[1]))
    finally:
        telnet.close()
