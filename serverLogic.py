import queue
from serverComm import ServerComm
import serverProtocol
import threading
import hashlib
import time


def request_for_new_range_to_check(ip, comm, params, current_range, clients, start_time, ranges_to_check):
   """
   the client asked for a new range to check - send a new range to the client
   :param ip: the clients ip
   :param comm: the object for communication
   :param params: None
   :param current_range: the next number that needs to be checked
   :param clients: dict of all clients (client_ip : range that is checking now)
   :param start_time: the time that it started checking the first range
   :param ranges_to_check: the q of the ranges that need to be checked again (client sent a wrong answer)
   :return: None
   """
   #if there is a range that needs to be checked again (client sent a wrong answer)
   if not ranges_to_check.empty():
       start_range, end_range = ranges_to_check.get()
       clients[ip] = (start_range, end_range)
       comm.send_msg(ip, serverProtocol.pack_range_to_check(start_range, end_range))

   #if there are still numbers that weren't checked
   elif current_range[0] < 9999999999:
        clients[ip] = (current_range[0], current_range[0]+10000)
        comm.send_msg(ip, serverProtocol.pack_range_to_check(current_range[0], current_range[0]+10000))
        current_range[0] = current_range[0] + 10000



def found_correct_answer(ip, comm, answer, current_range, clients, start_time, ranges_to_check):
    """
    the client found the correct number - checks if it is really the correct number and if it is prints it and stops clients
    :param ip: the clients ip
    :param comm: the object for communication
    :param answer: answer[0] = answer that the client found
    :param current_range: the next number that needs to be checked
    :param clients: dict of all clients (client_ip : range that is checking now)
    :param start_time: the time that it started checking the first range
    :param ranges_to_check: the q of the ranges that need to be checked again (client sent a wrong answer)
    :return: None
    """
    if hashlib.md5(answer[0].encode()).hexdigest() == "EC9C0F7EDCC18A98B1F31853B1813301".lower():
        print("number found: " + answer[0])

        current_time = time.time()
        time_that_took_to_find_ans = current_time - start_time
        print("time that took to find answer: " + str(time_that_took_to_find_ans))

        print("computer that found the answer: " + ip)
        print("num of cpus that worked on the answer: " + str(len(clients)))

        #stop the clients
        for client_ip in clients.keys():
            comm.send_msg(client_ip, serverProtocol.pack_answer_found())
    #if sent a wrong answer
    else:
        # add the range that the client checked to the q of ranges that need to be checked
        ranges_to_check.put(clients[ip])
        # disconnect the client
        comm.close_client(ip)
        # remove the client from the clients dictionary
        del clients[ip]

commands = {}
commands['1'] = request_for_new_range_to_check
commands['2'] = found_correct_answer

def handle_recv_msgs(comm, recvQ, current_range, clients, start_time, ranges_to_check):
    """
    handles messages based on opcode
    :param comm: the object for communication
    :param recvQ: the Q to receive messages
    :param game_state: dict of the game state
    :return: None
    """
    while True:
        ip, data = recvQ.get()
        opcode, params = serverProtocol.unpack(data)
        if opcode in commands.keys():
            commands[opcode](ip, comm, params, current_range, clients, start_time, ranges_to_check)




if __name__ == '__main__':
    recvQ = queue.Queue()
    #renges of clients that sent the wrong answer
    ranges_to_check = queue.Queue()
    comm = ServerComm(1001, recvQ)
    #mutebale
    current_range = [1000000000]
    #mutebale
    start_time = time.time()
    clients = {}
    threading.Thread(target=handle_recv_msgs, args=(comm, recvQ, current_range, clients, start_time, ranges_to_check)).start()
