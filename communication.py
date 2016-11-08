import logging
from os import getcwd
import socket
from text_and_log import setupLogger


def getIP():
    # Get the IP address of the computer executing this file
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_sock.connect(('192.168.0.1', 0))
    ip_address = temp_sock.getsockname()[0]
    temp_sock.close()
    return ip_address


class MessageVerification(object):
    def __init__(self, verbose=False):
        self.logger = setupLogger(verbose)

        self.logger.debug("All the errors of communication module will be logged in %s", getcwd())
        self.logger.debug("You can disable the verbosity by removing the 'verbose=True' from the MessageVerification() constructor.")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.timeout = None
        self.port = 65400
        self.backlog = 1  # maximum number of queued connections

    def setTimeout(self, seconds):
        self.timeout = seconds
        self.logger.info("Connection timeout changed to %s", seconds)

    def setPort(self, port_number):
        self.logger.info("Connection port has been changed to %s from %s", self.port_number, self.port)
        self.port = port_number
        self.logger.info("Make sure you also configure both ends of communication.")

    def setNumberOfConnections(self, number):
        self.backlog = number
        self.logger.info("Maximum number of queued connections changed to %s", number)

    def connectToServer(self, ip_address):
        self.logger.info("Connecting to the server on %s", ip_address)
        self.sock.settimeout(self.timeout)
        server_address = (ip_address, self.port)
        try:
            self.sock.connect(server_address)
            self.logger.info('Connected To %s.', server_address)
        except socket.error:
            logging.exception("Error in MessageVerification")
            print 'Connection failed. Check server.'
            raise

    def connectToClient(self, ip_address):
        self.logger.debug("Waiting for the client to be connected.")
        self.sock.settimeout(self.timeout)
        server_address = (ip_address, self.port)
        self.sock.bind(server_address)
        self.sock.listen(self.backlog)  # NOTE: maybe have to be changed in future
        try:
            self.sock, address = self.sock.accept()
            self.logger.info("Connection accepted from %s", address)
        except:
            logging.exception("Error in MessageVerification")
            print 'Connection failed. Check server.'
            raise

    def sendMessage(self, text):
        self.logger.debug("Sending: %s", text)
        self.sock.sendall(text)
        # sleep(1)
        self.logger.info("Sent: %s", text)

    def verifyMessage(self, text):
        self.logger.info("Waiting for message.")
        received_text = self.sock.recv(4096)
        self.logger.debug("Received: %s", received_text)
        if received_text == text:
            self.logger.info("Successful message verification: %s", text)
            return True
        else:
            self.logger.info("Failed to receive '%s', received '%s' instead.", text, received_text)
            return False

    def close(self):
        self.logger.debug("Closing the connection.")
        self.sock.close()
        self.logger.info("Connection closed.")
