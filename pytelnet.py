from socket import socket, AF_INET, SOCK_STREAM
from ssl import wrap_socket, PROTOCOL_SSLv23, SSLError
from sys import platform

CR = b'\r'
LF = b'\n'
CRLF = CR + LF
TIMEOUT = 1
BUFFER_SIZE = 512


class Client:
    def __init__(self, timeout=TIMEOUT, ssl=True):
        """
        Initialization

        :param timeout: Timeout (default - 1s)
        :param ssl: Use SSL connection (default - True)
        """
        self._SSL = ssl
        self._connection = socket(AF_INET, SOCK_STREAM)
        self._connection.settimeout(timeout)
        self._end_line = CRLF if platform is 'win32' else LF

    def connect(self, host, port):
        """
        Connection to host on port

        :param host: Address to connect
        :param port: Port to connect
        """
        try:
            if not self._SSL:
                raise SSLError
            ssl_connection = wrap_socket(self._connection, ssl_version=PROTOCOL_SSLv23)
            ssl_connection.connect((host, port))
            self._connection = ssl_connection
        except SSLError:
            self._connection.connect((host, port))

    def send(self, message):
        """
        Send message

        :param message: Text message
        """
        self._connection.send(message.encode() + self._end_line)

    def received(self):
        """
        Received message

        :return: Message
        """
        return self._connection.recv(BUFFER_SIZE).decode()

    def close(self):
        """
        Close connection
        """
        self._connection.close()
