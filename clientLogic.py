import os
import multiprocessing
import queue
from clientComm import ClientComm
import clientProtocol
import hashlib



def communicate_with_server():
    """

    :return:
    """
    recvQ = queue.Queue()
    comm = ClientComm("127.0.0.1", 1001, recvQ)
    # send to server that it needs first range
    comm.send_msg(clientProtocol.pack_request_for_more())
    handle_recv_msgs(recvQ, comm)


def new_range_to_check(comm, params):
    """

    :param comm:
    :param range:
    :return:
    """
    start, end = params
    start = int(start)
    end = int(end)
    for i in range(start, end):
        if hashlib.md5(str(i).encode()).hexdigest() == "EC9C0F7EDCC18A98B1F31853B1813301".lower():
            print("found", str(i))
            # sends the server that it got the right answer
            comm.send_msg(clientProtocol.pack_right_answer(str(i)))
    #send to server that it needs another range
    comm.send_msg(clientProtocol.pack_request_for_more())


def answer_found(comm, params):
    """

    :param comm:
    :param params:
    :return:
    """
    comm.closeClient()


commands = {}
commands['1'] = new_range_to_check
commands['2'] = answer_found




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
        print("opcode:", repr(opcode))
        print("params:", repr(params))
        if opcode in commands.keys():
            commands[opcode](comm, params)


if __name__ == "__main__":

    # num of cores that the computer has
    num_cores = os.cpu_count()

    for i in range(num_cores):
        process = multiprocessing.Process(target=communicate_with_server, args=())
        #start the process
        process.start()