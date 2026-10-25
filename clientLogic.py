#https://github.com/AmitNutman/BruteForce



import os
import multiprocessing
import queue
from clientComm import ClientComm
import clientProtocol
import hashlib



def communicate_with_server(str_to_look_for):
    """
    creates comm to communicate with server and ask for starting range
    :str_to_look_for: list
    :str_to_look_for: the str that it needs to look for
    :return: None
    """
    recvQ = queue.Queue()
    comm = ClientComm("127.0.0.1", 1001, recvQ)
    #let server know it was connected - to get str to find
    comm.send_msg(clientProtocol.pack_connected_msg())
    handle_recv_msgs(recvQ, comm, str_to_look_for)



def new_range_to_check(comm, params, str_to_look_for):
    """
    checks the range
    :param comm: the object for communication
    :param params: tuple - start_range, end_range
    :str_to_look_for: the str that it needs to look for
    :return: None
    """
    start, end = params
    print("working on: " + start + "-" + end)
    start = int(start)
    end = int(end)
    found = False
    for i in range(start, end):
        if hashlib.md5(str(i).encode()).hexdigest() == str_to_look_for[0].lower():
            found = True
            # sends the server that it got the right answer
            comm.send_msg(clientProtocol.pack_right_answer(str(i)))
            break
    if not found:
        #send to server that it needs another range
        comm.send_msg(clientProtocol.pack_request_for_more())


def answer_found(comm, params, str_to_look_for):
    """
    closes the client because the answer was found
    :param comm: the object for communication
    :param params:None
    :str_to_look_for: the str that it needs to look for
    :return: None
    """
    print("closed")
    comm.close_client()


def got_str_to_look_for(comm, params, str_to_look_for):
    """
    gets the str that it needs to look for and asks for first range
    :param comm: the object for communication
    :param params:params[0] = str_to_look_for
    :str_to_look_for: the str that it needs to look for - has None right now
    :return: None
    """
    str_to_look_for[0] = params[0]
    # send to server that it needs first range
    comm.send_msg(clientProtocol.pack_request_for_more())



commands = {}
commands['1'] = new_range_to_check
commands['2'] = answer_found
commands['3'] = got_str_to_look_for




def handle_recv_msgs(recvQ, comm, str_to_look_for):
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
            commands[opcode](comm, params, str_to_look_for)
        if opcode == "2":
            break

if __name__ == "__main__":

    # num of cores that the computer has
    num_cores = os.cpu_count()

    # mutebale
    str_to_look_for = [""]

    for i in range(num_cores):
        process = multiprocessing.Process(target=communicate_with_server, args=(str_to_look_for,))
        #start the process
        process.start()