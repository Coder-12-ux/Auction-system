from common import *
import socket
import threading


class Participant:
    def __init__(self, name, address):
        self.name, self.address = name, address
        self.details = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_server = True
        self.bids = 0
        self.auction_data = {}

    def send(self, abc):
        """sends messages/commands to auction server"""
        self.socket.send(bytes(abc, FORMAT))

    def bid(self, price=""):
        """sends the command to increase the bid"""
        self.send("+"+price)

    def listen(self):
        """Starts listening to the auction server"""
        from json import loads
        while self.listen_server:
            message = self.socket.recv(512).decode(FORMAT)

            if message.startswith("@uction_data"):
                self.auction_data = loads(message[len("@uction_data"):])

            if message == DISCONNECT_MESSAGE:
                self.listen_server = False

    def start(self):
        """Starts the participant to send & receive commands to the auction server"""
        self.socket.connect(self.address)
        # this thread will listen the commands from server
        listen = threading.Thread(target=self.listen)
        listen.start()  # listening starts
        self.socket.send(bytes(f"|{self.name}", FORMAT))


if __name__ == "__main__":
    p = Participant("Vipul", ("localhost", 60000))
    p.start()
