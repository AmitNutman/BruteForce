import socket
import threading
import select
from diffieHelman import DiffieHelman
from AES import AESCipher



class ServerComm():
    def __init__(self, port, recvQ):
        """
        constructor
        :param port: the port to listen to
        :param recvQ: the q of msg
        """
        self.server = socket.socket()
        self.recvQ = recvQ
        self.open_clients = {}
        self.client_ip_counter = 1 #counter for some clients with the same ip
        threading.Thread(target = self._mainLoop, args=(port,)).start()


    def _mainLoop(self, port):
        """
        receive the messages
        :param port: the port to communicate with
        :return: None
        """
        # connects the server to this port so clients can connect to it
        self.server.bind(("0.0.0.0", port))
        # waits for clients to try to connect to the server (up to 4 waiting)
        self.server.listen(4)
        # recv the messages - first length in len of 6 bytes than data in len of length
        # recv data in bytes encrypted - decrypt data and decodes data
        while True:
            # checks which sockets are ready:
            # rlist - sockets ready to read (new connection or incoming data)
            # wlist - sockets ready to send data
            # xlist - sockets with errors
            # includes the server socket (for new clients) and client sockets (for messages)
            # allows handling multiple clients without blocking by checking who is ready instead of waiting
            # timeout 0.01 makes it non-blocking (keeps the loop running)
            rlist, wlist, xlist = select.select([self.server] + list(self.open_clients.keys()), self.open_clients.keys(), [], 0.01)
            # for every socket in sockets ready to read (new connection or incoming data)
            for current_sock in rlist:
                # if its self.server, this means there is a new connection
                if current_sock is self.server:
                    # accepts a new client connection and returns its socket and addr
                    client, addr = self.server.accept()
                    print(f"{addr[0]} - connected")
                    # create key to encrypt and decrypt and in the function add ip to the dictionary
                    threading.Thread(target=self._handle_keys, args=(client, addr[0])).start()
                # else there is incoming data
                else:
                    try:
                        data_len = int(current_sock.recv(6).decode())
                        data = current_sock.recv(data_len)
                    except Exception as e:
                        print(f"in main loop - {str(e)}")
                        data = ""
                    if data == "":
                        self._close_client(current_sock)
                    else:
                        if current_sock in self.open_clients.keys():
                            data = self.open_clients[current_sock][1].decrypt_file(data).decode()
                            # adds to Q the ip and msg (as string, decrypted) - opens this msg from Q in serverLogic
                            self.recvQ.put((self.open_clients[current_sock][0], data))



    def _handle_keys(self, sock, ip):
        """
        finds key and add to dictionary
        :param sock: the servers sock
        :param ip: the ip of client
        :return: None
        """
        # 1. Both sides use public numbers and a private secret_key to generate a public mix.
        # 2. They exchange these mixed keys over the network, keeping their secret_keys safe.
        # 3. Each side combines the received key with its own secret_key to calculate the exact same shared encryption key.
        try:
            # the public mixed key received from the client
            length = int(sock.recv(6).decode())
            key1 = int(sock.recv(length).decode())
        except Exception as e:
            print(f"in handle_keys - {str(e)}")
            self._close_client(sock)
        df = DiffieHelman(3, 257)

        # Calculates the final shared secret using the client's public key
        shared_key = str(df.calc_key_2(key1))


        # if ip exists, add a counter at the end of ip
        ip_exist = False
        for open_client_ip, AES in self.open_clients.values():
            if ip == open_client_ip:
                ip_exist = True
                break
        if ip_exist:
            ip = ip + f"_{self.client_ip_counter}"
            self.client_ip_counter += 1
        # adds ip and key to dict of open_clients
        self.open_clients[sock] = [ip, AESCipher(shared_key)]

        # calculates the server's public mixed key
        key1_toSend = df.calc_key_1()
        # sends the public mixed key to the client
        key_to_send = str(key1_toSend)
        msg_len = str(len(key_to_send)).zfill(6)
        try:
            sock.send(msg_len.encode())
            sock.send(key_to_send.encode())
        except Exception as e:
            print(f"in handle_keys - {str(e)}")
            self._close_client(sock)



    def _close_client(self, client_soc):
        """
        closes the clients socket
        :param client_soc: the client socket to close
        :return: None
        """
        if client_soc in self.open_clients.keys():
            print(f"{self.open_clients[client_soc]} - disconnected")
            del self.open_clients[client_soc]
            client_soc.close()




    def find_ip_by_soc(self, ip):
        """
        finds the socket based on its ip
        :param ip: the ip to find
        :return: Socket
        """
        sock = None
        for client_sock in self.open_clients.keys():
            if self.open_clients[client_sock][0] == ip:
                sock = client_sock
                break
        return sock


    def close_client(self, ip):
        """
        closes the client based on ip
        :param ip: the ip of the client
        :return: None
        """
        sock = self.find_ip_by_soc(ip)
        if sock:
                self._close_client(sock)


    def send_msg(self, ip, msg):
        """
        sends the message to client
        :param ip: the ip to send to
        :param msg: the msg to send
        :return: None
        """
        sock = self.find_ip_by_soc(ip)
        if sock:
            # if str - encode, else (img) already bytes - don't need to encode
            if isinstance(msg, str):
                msg = msg.encode()
            # encrypts the msg
            encrypted_msg = self.open_clients[sock][1].encrypt_bytes(msg)
            # calculates the length of encrypted msg - different from len of not encrypted msg
            msg_len = str(len(encrypted_msg)).zfill(6)
            try:
                sock.send(msg_len.encode())
                sock.send(encrypted_msg)
            except Exception as e:
                print(f"in send msg - {str(e)}")
                self._close_client(sock)
