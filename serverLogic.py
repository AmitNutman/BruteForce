import queue
from serverComm import ServerComm
import serverProtocol
import threading
import hashlib

def request_for_new_range_to_check(ip, comm, params, current_range):
   """

   :param ip:
   :param comm:
   :param params:
   :param current_range:
   :return:
   """
   #if there are still numbers that weren't checked
   if current_range[0] < 9999999999:
        comm.send_msg(ip, serverProtocol.pack_range_to_check(current_range[0], current_range[0]+100000000))
        current_range[0] = current_range[0] + 100000000

def found_correct_answer(ip, comm, answer, current_range):
    if hashlib.md5(answer[0].encode()).hexdigest() == "EC9C0F7EDCC18A98B1F31853B1813301".lower():
        print(answer[0])

commands = {}
commands['1'] = request_for_new_range_to_check
commands['2'] = found_correct_answer

def handle_recv_msgs(comm, recvQ, current_range):
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
            commands[opcode](ip, comm, params, current_range)




if __name__ == '__main__':
    recvQ = queue.Queue()
    comm = ServerComm(1001, recvQ)
    #mutebale
    current_range = [1000000000]
    threading.Thread(target=handle_recv_msgs, args=(comm, recvQ, current_range)).start()
