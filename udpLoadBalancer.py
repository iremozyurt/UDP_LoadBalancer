import time
from socket import *

class udpLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_server_index = 0

    def save_state(self, filename='state.txt'):
        with open(filename, 'w') as file:
            file.write(str(self.current_server_index))

    def load_state(self, filename='state.txt'):
        try:
            with open(filename, 'r') as file:
                self.current_server_index = int(file.read())
        except FileNotFoundError:
            pass

    def get_next_server(self):
        server = self.servers[self.current_server_index]
        self.current_server_index = (self.current_server_index + 1) % len(self.servers)
        return server

    def balance_pings(self, num_pings):
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(1)

        for i in range(num_pings):
            server_addr = self.get_next_server()
            remoteAddr = (server_addr[0], int(server_addr[1]))

            sendTime = time.time()
            message = f'PING {i + 1} {time.strftime("%H:%M:%S")} (This message from load balancer!!!) The port of the server is {remoteAddr[1]}'
            clientSocket.sendto(bytes(message, 'utf-8'), remoteAddr)

            try:
                data, server = clientSocket.recvfrom(1024)
                recdTime = time.time()
                rtt = recdTime - sendTime
                print("Message Received", data)
                print("Round Trip Time", rtt)
            except timeout:
                print('REQUEST TIMED OUT')


        self.save_state()

if __name__ == "__main__":
    servers = [('localhost', 2526), ('localhost', 2527), ('localhost', 2528)]
    load_balancer = udpLoadBalancer(servers)
    load_balancer.balance_pings(10)
