#https://github.com/AmitNutman/BruteForce


import os
import multiprocessing
import queue
from clientComm import ClientComm
import clientProtocol
import hashlib



def communicate_with_server():
    """
    creates comm to communicate with server and ask for starting range
    :return: None
    """
    recvQ = queue.Queue()
    comm = ClientComm("127.0.0.1", 1001, recvQ)
    # send to server that it needs first range
    comm.send_msg(clientProtocol.pack_request_for_more())
    handle_recv_msgs(recvQ, comm)


def new_range_to_check(comm, params):
    """
    checks the range
    :param comm: the object for communication
    :param params: tuple - start_range, end_range
    :return: None
    """
    start, end = params
    print("working on: " + start + "-" + end)
    start = int(start)
    end = int(end)
    found = False
    for i in range(start, end):
        if hashlib.md5(str(i).encode()).hexdigest() == "EC9C0F7EDCC18A98B1F31853B1813301".lower():
            found = True
            # sends the server that it got the right answer
            comm.send_msg(clientProtocol.pack_right_answer(str(i)))
            break
    if not found:
        #send to server that it needs another range
        comm.send_msg(clientProtocol.pack_request_for_more())


def answer_found(comm, params):
    """
    closes the client because the answer was found
    :param comm: the object for communication
    :param params:
    :return: None
    """
    print("closed")
    comm.close_client()

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
        if opcode in commands.keys():
            commands[opcode](comm, params)
        if opcode == "2":
            break

if __name__ == "__main__":

    # num of cores that the computer has
    num_cores = os.cpu_count()

    for i in range(num_cores):
        process = multiprocessing.Process(target=communicate_with_server, args=())
        #start the process
        process.start()