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

    :return:
    """
    return f"2#!#{answer}"



def pack_request_for_more():
    """

    :return:
    """
    return "1"
