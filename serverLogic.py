import queue
from serverComm import ServerComm
import serverProtocol

commands = {}
commands['1'] = request_for_new_range_to_check
commands['2'] = found_correct_answer

def handle_recv_msgs(comm, recvQ):
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
            commands[opcode](ip, comm, data)




if __name__ == '__main__':
    recvQ = queue.Queue()
    comm = ServerComm(1001, recvQ)
