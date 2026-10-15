import queue
from serverComm import ServerComm







if __name__ == '__main__':
    recvQ = queue.Queue()
    comm = ServerComm(1001, recvQ)
