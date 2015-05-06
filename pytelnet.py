#!/usr/bin/python3

"""
TELNET written in Python
"""

import argparse
import socket
import ssl
import sys

# Product: PyTelnet
# Copyright (C) 2015 LeMarck (https://github.com/LeMarck)
# Author: Petrov E.S.
# Contact: jeysonep@gmail.com


__author__ = 'Evgeny Petrov'

__version__ = '1.0'


CR = b'\r'
LF = b'\n'
CRLF = CR + LF
TIMEOUT = 1


def main(host, port):
    """

    :param host: - Address to connect
    :param port: - Port to connect
    :return:
    """
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(TIMEOUT)
        connection = ssl.wrap_socket(connection,
                                     ssl_version=ssl.PROTOCOL_SSLv23)
        connection.connect((host, port))
    except ssl.SSLError:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.settimeout(TIMEOUT)
        connection.connect((host, port))
    except Exception as e:
        sys.exit(e)

    try:
        print(connection.recv(512)[:-2].decode())
    except socket.timeout:
        pass
    except Exception as e:
        connection.close()
        sys.exit(e)

    while True:
        request = input()
        if request == '\n':
            continue
        connection.send(request.encode()+CRLF)

        try:
            while True:
                answer = connection.recv(512)[:-2]
                if not answer:
                    sys.exit()
                print(answer.decode())
        except socket.timeout:
            # print('')
            pass
        except Exception as e:
            print(e)

    connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', type=str, help='The host name or IP address'
                                               ' of the remote computer to '
                                               'which you are connecting.')
    parser.add_argument('port', type=int, help='The port number or '
                                               'service name.')

    args = parser.parse_args()

    try:
        main(args.host, args.port)
    except KeyboardInterrupt:
        sys.exit("Connection terminated")
    except Exception as e:
        sys.exit('Can not connect to "{}"'.format(sys.argv[1]))
