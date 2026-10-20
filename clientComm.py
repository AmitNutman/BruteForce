#https://github.com/AmitNutman/BruteForce



import socket
import threading
from diffieHelman import DiffieHelman
from AES import AESCipher
import time



class ClientComm():
    def __init__(self, serverIp, port, recvQ):
        """
        constructor
        :param serverIp: the server's ip
        :param port: the port
        :param recvQ: the q of msg
        """
        self.my_sock = socket.socket()
        self.recvQ = recvQ
        self.my_AES = None
        threading.Thread(target=self._mainLoop, args=(serverIp,port,)).start()


    def _mainLoop(self, serverIp, port):
        """
        receive the messages
        :param serverIp: the ip
        :param port: port
        :return: None
        """
        # connects the client socket to the server using IP and port
        try:
            self.my_sock.connect((serverIp,port))
        except Exception as e:
            print(f"in connect {str(e)}")
            exit("server is down - try later")
        # creates unique key to communicate the server with - for encrypt, decrypt
        self.create_key()

        # recv the messages - first length in len of 6 bytes than data in len of length
        # recv data in bytes encrypted - decrypt data and leave it in byte (decode data in clientProtocol if needed)
        while True:
            try:
                data_len = int(self.my_sock.recv(6).decode())
            except Exception as e:
                print(f"in main loop - {str(e)}")
                data_len = 0
            if data_len == 0:
                self.close_client()
                break
            else:
                data = b""
                # recv in loop of 1024 every chunk because gets pictures as well
                while len(data) < data_len:
                    to_read = min(1024, data_len - len(data))
                    try:
                        chunk = self.my_sock.recv(to_read)
                    except Exception as e:
                        print(f"in main loop - {str(e)}")
                        self.close_client()
                    if not chunk:
                        self.close_client()
                        break
                    data += chunk
                data = self.my_AES.decrypt_file(data)
                #adds to Q the msg (as bytes, decrypted) - opens this msg from Q in clientLogic
                self.recvQ.put(data)



    def create_key(self):
        """
        create key to encrypt and decrypt
        :return: None
        """
        # 1. Both sides use public numbers and a private secret_key to generate a public mix.
        # 2. They exchange these mixed keys over the network, keeping their secret_keys safe.
        # 3. Each side combines the received key with its own secret_key to calculate the exact same shared encryption key.
        df = DiffieHelman(3, 257)
        # calculates the client's public mixed key
        key1 = df.calc_key_1()
        # sends the public mixed key to the server
        msg2send = str(key1)
        try:
            self.my_sock.send(str(len(msg2send)).zfill(6).encode())
            self.my_sock.send(msg2send.encode())
            length = int(self.my_sock.recv(6).decode())
            data = self.my_sock.recv(length)
        except Exception as e:
            print(f"in create_key - {str(e)}")
            self.close_client()
        # the server's public mixed key received from the network
        server_key = int(data)
        # calculates the final shared secret and creates the AES cipher
        self.my_AES = AESCipher(str(df.calc_key_2(server_key)))


    def close_client(self):
        """
        closes the client
        :return: None
        """
        print("client disconnected")
        self.my_sock.close()
        #lets gui know there is a problem e=with the connection
        self.recvQ.put("X".encode())



    def send_msg(self, msg):
        """
        sends the msg to server
        :param msg: the msg to send
        :return: None
        """
        # if AES(key) still hasn't created - wait 0.1 sec (we need it for this function to encrypt)
        while self.my_AES is None:
            time.sleep(0.1)
        if isinstance(msg, str):
            data = msg.encode()
        else:
            data = msg
        #encrypts the msg
        data = self.my_AES.encrypt_bytes(data)
        #calculates the length of encrypted msg - different from len of not encrypted msg
        msg_len = str(len(data)).zfill(6)
        try:
            self.my_sock.send(msg_len.encode())
            self.my_sock.send(data)
        except Exception as e:
            print(f"in send msg - {str(e)}")
            self.close_client()




