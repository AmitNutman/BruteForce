import os
import multiprocessing
import queue
from clientComm import ClientComm
import clientProtocol



def communicate_with_server():
    """

    :return:
    """
    recvQ = queue.Queue()
    comm = ClientComm("127.0.0.1", 1001, recvQ)


commands = {}
commands['1'] = new_range_to_check



def handle_recv_msgs(recvQ, comm):
    """
    handles messages based on opcode
    :param recvQ: the Q to receive messages from server
    :param comm: the object for communication
    :return: None
    """
    while True:
        data = recvQ.get()
        opcode, params = clientProtocol.unpack(data)
        if opcode in commands.keys():
            commands[opcode](comm, params)


if __name__ == "__main__":

    # num of cores that the computer has
    num_cores = os.cpu_count()

    for i in range(num_cores):
        process = multiprocessing.Process(target=communicate_with_server, args=())
        #start the process
        process.start()