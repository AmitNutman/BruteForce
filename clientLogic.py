import os
import multiprocessing
import queue
from clientComm import ClientComm



def communicate_with_server():
    """

    :return:
    """
    recvQ = queue.Queue()
    comm = ClientComm("127.0.0.1", 1001, recvQ)


if __name__ == "__main__":

    # num of cores that the computer has
    num_cores = os.cpu_count()

    for i in range(num_cores):
        process = multiprocessing.Process(target=communicate_with_server, args=())
        #start the process
        process.start()