def unpack(data):
    """
    unpacks the package
    :param data: the package to unpack
    :return: tuple (opcode, params)
    """
    opcode = data[0:1].decode()
    params = data.decode().split("#!#")[1:]
    return (opcode, params)


def pack_right_answer(answer):
    """
    packs the right answer to send to server
    :param answer: the answer
    :return: str
    """
    return f"2#!#{answer}"



def pack_request_for_more():
    """
    pack a request for another range
    :return: str - the request
    """
    return "1"
